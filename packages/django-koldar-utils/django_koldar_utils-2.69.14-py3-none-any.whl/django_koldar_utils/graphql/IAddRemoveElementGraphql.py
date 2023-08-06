import abc
from typing import Dict, Optional, List, Tuple, Union

import stringcase

import graphene

from django_koldar_utils.django import django_helpers
from django_koldar_utils.graphql import error_codes
from django_koldar_utils.graphql.GraphQLAppError import GraphQLAppError
from django_koldar_utils.graphql.GraphQLHelper import GraphQLHelper


class AddMutationContext(object):

    def __init__(self, django_types: List[type], graphene_types: List[type], graphene_input_types: List[type], relation_name: str, add_if_not_present: bool):
        self.django_types = django_types
        self.graphene_types = graphene_types
        self.graphene_input_types = graphene_input_types
        self.relation_name = relation_name
        self.add_if_not_present = add_if_not_present


class RemoveMutationContext(object):

    def __init__(self, django_types: List[type], graphene_types: List[type], graphene_input_types: List[type], relation_name: str,
                 ignore_if_not_present: bool):
        self.django_types = django_types
        self.graphene_types = graphene_types
        self.graphene_input_types = graphene_input_types
        self.relation_name = relation_name
        self.ignore_if_not_present = ignore_if_not_present


class IAddRemoveElementGraphql(abc.ABC):
    """
    A class that generates classes representing graphql queries adding adn removing items from a relationship.
    Relationship can
    """

    @abc.abstractmethod
    def _add_object_to_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext],
                          data_type: type, data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        """
        Add an object passed in input to the database.
        By default we will call create with data

        :param mutation_class: mutation class that we are building
        :param django_element_type: django element, passed from generate
        :param data: set of input parameters fo the graphql mutation
        :param info: graphql info
        :param args: graphql args
        :param kwargs: graphql kwargs
        :return: true if the object is already present in the database, false otherwise.
        """
        pass

    @abc.abstractmethod
    def _is_object_in_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext],
                          data_type: type, data: Dict[str, any], info, *args, **kwargs) -> bool:
        """
        :return: true if the object is inside the database, false otherwise
        """
        pass

    @abc.abstractmethod
    def _get_object_from_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext],
                          data_type: type, data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        """
        Add an object passed in input to the database.
        By default we will call create with data

        :param mutation_class: mutation class that we are building
        :param django_element_type: django element, passed from generate
        :param active_flag_name: name of the flag which is true if the row exists, false toherwise
        :param data_type: django model type of the object to generate
        :param data: set of input parameters fo the graphql mutation
        :param info: graphql info
        :param args: graphql args
        :param kwargs: graphql kwargs
        :return: the object from the database
        """
        pass

    @abc.abstractmethod
    def _get_number_of_elements_in_association(self, context: Union[AddMutationContext, RemoveMutationContext]) -> int:
        """
        :param context: context of the mutation generation
        :return: number of elements in the given association
        """
        pass

    @abc.abstractmethod
    def _add_association_between_models_in_db(self, context: AddMutationContext, object_to_adds: Dict[type, any]) -> Tuple[any, int]:
        """
        :param context: context of the mutation generation
        :return: pair
         - an object that will be put in the output of the mutation
         - number of elements added in the association
        """
        pass

    @abc.abstractmethod
    def _remove_association_between_models_from_db(self, mutation_class: type, context: RemoveMutationContext,
                          data: Dict[str, any], info, *args, **kwargs) -> List[any]:
        """
        Concretely remove the association of a given relationship

        :return: a list of elements removed from the association. You can return whatever you want. The concatenation
        of these values will be returned from this mutation
        """
        pass

    @abc.abstractmethod
    def _get_remove_mutation_primary_input_list(self, context: RemoveMutationContext) -> graphene.Field:
        """
        :return: an element that will belong to the mutation remove graphql input parameters. This
            element contains the list of elements to remove from the association
        """
        pass

    @abc.abstractmethod
    def _get_remove_mutation_primary_output_list(self, context: RemoveMutationContext) -> graphene.Field:
        """
        :return: a list of elements that will be returned from the outptu of the mutation.
            It can be whatever you want
        """
        pass

    def _models_active_flag_name(self, context: Union[AddMutationContext, RemoveMutationContext]) -> str:
        """
        :param context: context of the mutation generation
        :return: name of the flag that represents whether or not the row should be considered or not
        """
        return "active"

    def _get_add_mutation_input_parameter_names(self, context: AddMutationContext) -> List[Tuple[type, str]]:
        """
        :return: name of the graphql mutation parameter representing the object to add.
        The object return as many values as the size of the relationship. first item of pairs are django types and
        second item pairs are the input parameter types
        """
        return [(k, stringcase.pascalcase(f"{k.__name__}Item")) for k in context.graphene_input_types]

    def _get_add_mutation_output_return_value_name(self, context: AddMutationContext) -> str:
        """
        :return: name of the return value of the add mutation
        """
        return f"{context.relation_name}AddOutcome"

    def _get_fields_to_check(self, context: Union[AddMutationContext, RemoveMutationContext]) -> List[
        graphene.Field]:
        """
        :return: parameters in the graphql mutation input parameter representing unique fields. Useful for checking if
            a value has already been added to the database
        """
        return list(django_helpers.get_unique_field_names(context.django_secondary_owner_type))

    def _get_old_length_output_name(self, context: Union[AddMutationContext, RemoveMutationContext]) -> str:
        return f"{context.relation_name}OldLength"

    def _new_length_output_name(self, context: Union[AddMutationContext, RemoveMutationContext]) -> str:
        return f"{context.relation_name}NewLength"

    def _added_output_name(self, context: AddMutationContext) -> str:
        return f"{context.relation_name}Added"

    def _created_output_name(self, context: AddMutationContext) -> str:
        return f"{context.relation_name}Created"

    @abc.abstractmethod
    def _add_mutation_output_graphene_field(self, context: AddMutationContext) -> graphene.Field:
        """
        :return: graphene declaration of the output
        """
        pass
        return GraphQLHelper.returns_nonnull(
            return_type=context.graphene_types[0],
            description=f"the {context.graphene_types[0].__name__} we just added in the relation"
        )

    def _convert_graphql_input_to_dict(self, graphql_input: any, fields_to_check: List[graphene.Field]) -> Dict[str, any]:
        result = dict()
        for f in fields_to_check:
            if not hasattr(graphql_input, f.name):
                continue
            result[f.name] = getattr(graphql_input, f.name)
        return result

    def generate(self, graphene_types: List[type],
                 graphene_input_types: List[type], relation_name: str,
                 add_if_not_present: bool = False,
                 generate_add_mutation: bool = True,
                 generate_remove_mutation: bool = True,
                 ) -> Tuple[type, type]:
        """
        :param graphene_main_owner_type: django type owning a list of items of type django_element_owner_type
        :param graphene_secondary_types: django type of the array of list. If the relations is more than binary,
        :param relation_name: name of the relationship represented by the list
        :param graphene_secondary_input_types: graphene type representing a single cell in the list owned by django_list_owner_type. The type represents a graphql input type.
        :param add_if_not_present: if this variable is set to True, if the user add a non persisteed django_element_type instance as the input of the mutation,
            we will first persist such an object
        :param generate_remove_mutation: if set, we will create a remove mutation
        :param generate_add_mutation: if set, we will create an add mutation
        :reutrn: first type representing this add element to list mutation, while the second represents the removal from this list
        """

        django_types = [x._meta.model for x in graphene_types]

        if generate_add_mutation:
            add_mutation = self._generate_add_mutation(AddMutationContext(
                django_types=django_types,
                graphene_types=graphene_types,
                graphene_input_types=graphene_input_types,
                relation_name=relation_name,
                add_if_not_present=add_if_not_present,
            ))
        else:
            add_mutation = None

        if generate_remove_mutation:
            remove_mutation = self._generate_remove_mutation(RemoveMutationContext(
                django_types=django_types,
                graphene_types=graphene_types,
                graphene_input_types=graphene_input_types,
                relation_name=relation_name,
                ignore_if_not_present=True,
            ))
        else:
            remove_mutation = None

        return add_mutation, remove_mutation

    def _generate_add_mutation(self, context: AddMutationContext) -> type:

        description = self._get_add_mutation_description(context)
        active_flag_name = self._models_active_flag_name(context)
        input_names = self._get_add_mutation_input_parameter_names(context)
        output_name = self._get_add_mutation_output_return_value_name(context)
        fields_to_check = self._get_fields_to_check(context)
        old_length_output_name = self._get_old_length_output_name(context)
        new_length_output_name = self._new_length_output_name(context)
        added_output_name = self._added_output_name(context)
        created_output_name = self._created_output_name(context)

        mutation_class_name = self._add_mutation_name(context)

        def body(mutation_class, info, *args, **kwargs) -> any:
            nonlocal self
            result_create = False

            # create data
            input_values = [input_class(kwargs[input_param_name]) for input_class, input_param_name in input_names]
            input_as_dict_data = dict()
            for input_value in input_values:
                d = self._convert_graphql_input_to_dict(input_value, fields_to_check)
                # automatically add active flag
                d[active_flag_name] = True
                input_as_dict_data[type(input_value)] = d

            # iterate over input_values and create the relationship point if necessary
            objects_to_add = dict()
            for single_data_type, single_data in input_as_dict_data.items():
                # check if the element we need to add exists in the database
                if not self._is_object_in_db(mutation_class, context, single_data_type, single_data, info, *args, **kwargs):
                    if context.add_if_not_present:
                        # we need to create the object
                        # create argument and omits the None values
                        create_args = {k: v for k, v in dict(single_data).items() if v is not None}
                        object_to_add = self._add_object_to_db(mutation_class, context, single_data_type, create_args,
                                                               info, *args, **kwargs)
                        if object_to_add is None:
                            raise GraphQLAppError(error_codes.CREATION_FAILED, object=single_data_type.__name__,
                                                  values=create_args)
                        result_create = True
                    else:
                        raise GraphQLAppError(error_codes.OBJECT_NOT_FOUND, object=single_data_type.__name__, values=single_data)
                else:
                    object_to_add = self._get_object_from_db(
                        mutation_class=mutation_class,
                        context=context,
                        data_type=single_data_type,
                        data=single_data,
                        info=info,
                        *args, **kwargs
                    )
                objects_to_add[single_data_type] = object_to_add

            # ok, now add the relationship (if needed)
            result, added = self._add_association_between_models_in_db(
                context=context,
                objects_to_add=objects_to_add
            )

            new_len = self._get_number_of_elements_in_association(
                context=context,
            )
            old_len = new_len - added
            result_added = new_len > old_len

            # yield result
            return mutation_class(**{
                output_name: result,
                added_output_name: result_added,
                created_output_name: result_create,
                old_length_output_name: old_len,
                new_length_output_name: new_len
            })

        arguments = dict()

        for input_class, input_param in input_names.items():
            arguments[input_param] = GraphQLHelper.argument_required_input(
                input_type=input_class,
                description=f"one of the endpoints of the relation {context.relation_name}"
            )

        arguments = self._configure_add_mutation_inputs(arguments, context)

        return GraphQLHelper.create_mutation(
            mutation_class_name=str(mutation_class_name),
            description=description,
            arguments=arguments,
            return_type={
                output_name: self._add_mutation_output_graphene_field(context),
                added_output_name: GraphQLHelper.returns_required_boolean(
                    description=f"True if we had added a new item in the collection, false otherwise"),
                created_output_name: GraphQLHelper.returns_required_boolean(
                    description=f"True if we had created the new item in the database before adding it to the relation"),
                old_length_output_name: GraphQLHelper.returns_required_int(
                    description=f"The number of elements in the collection before the add operation was performed"),
                new_length_output_name: GraphQLHelper.returns_required_int(
                    description=f"The number of elements in the collection after the add operation was performed"),
            },
            body=body
        )

    def _configure_add_mutation_inputs(self, original_arguments: Dict[str, graphene.Field], context: AddMutationContext) -> Dict[
        str, graphene.Field]:
        return original_arguments

    def _configure_remove_mutation_inputs(self, original_arguments: Dict[str, graphene.Field], context: RemoveMutationContext) -> Dict[
        str, graphene.Field]:
        return original_arguments

    def _get_add_mutation_description(self, context: AddMutationContext) -> str:
        if context.add_if_not_present:
            not_present = "We will persist it first by creating the object"
        else:
            not_present = "We will raise exception"
        dsc = f"""Allows to add a new association of the relation {context.relation_name} for the type {', '.join(map(lambda x: x.__name__, context.django_types))}. If an element
            is already within such a list we do nothing. If the element input that is an endpoint for this assoication 
            is not already persisted in the database (i.e., the input has an id not null), {not_present}. 
            If the item to add has the active flag set to False, we do nothing. 
            The function returns the element added in the relationship as well as the previous and after length of the
            collection w.r.t. the add operation. We will also return whether or not we actually have added the
            new item to the collection and if we had to first create a new item in the database.
            """
        return dsc

    def _get_remove_mutation_description(self, context: RemoveMutationContext) -> str:
        if context.ignore_if_not_present:
            not_present = "we will do nothing"
        else:
            not_present = "we will raise exception"
        dsc = f"""Allows to remove a relationship between the objects 
            {', '.join(map(lambda x: x.__name__, context.django_types))} previously created. 
            The relationship involved is \"{context.relation_name}\". If we are 
            requested to remove an element which is not in the list, {not_present}. 
            If the item to remove exists and has the active flag set to False, we do nothing. 
            The function returns the element added in the relationship as well as the previous and after length
            of the collection w.r.t. the remove operation. We will also return whether or not we actually 
            have removed the item to the collection. With this mutation you can remove multiple items in one sweep.
            """
        return dsc

    def _get_remove_mutation_input_parameter_name(self, context: RemoveMutationContext) -> str:
        """
        :return: name of the graphql mutation parameter representing the object to add
        """
        return "itemsToRemove"

    def _get_remove_mutation_output_return_value_name(self, context: RemoveMutationContext) -> str:
        """
        :return: name of the return value of the add mutation
        """
        return f"{stringcase.camelcase(context.relation_name)}RemoveOutcome"

    def _add_mutation_name(self, context: AddMutationContext) -> str:
        """
        Generate the name of the class representing the add mutation
        """
        return f"Add{stringcase.pascalcase(context.relation_name)}Of{''.join(map(lambda x: stringcase.pascalcase(x.__name__), context.django_types))}"

    def _remove_mutation_name(self, context: RemoveMutationContext) -> str:
        """
        Generate the name of the class representing the add mutation
        """
        return f"Remove{stringcase.pascalcase(context.relation_name)}Of{''.join(map(lambda x: stringcase.pascalcase(x.__name__), context.django_types))}"

    def _generate_remove_mutation(self, context: RemoveMutationContext) -> type:

        description = self._get_remove_mutation_description(context)
        active_flag_name = self._models_active_flag_name(context)
        input_name = self._get_remove_mutation_input_parameter_name(context)
        output_name = self._get_remove_mutation_output_return_value_name(context)
        fields_to_check = self._get_fields_to_check(context)
        old_length_output_name = self._get_old_length_output_name(context)
        new_length_output_name = self._new_length_output_name(context)

        mutation_class_name = self._remove_mutation_name(context)

        def body(mutation_class, info, *args, **kwargs) -> any:
            nonlocal self
            result_create = False

            # input parameter is a list
            input_parameter = kwargs[input_name]
            # for every element in the list "input_parameter", we try to remove it
            elements_removed = []
            for x in input_parameter:
                d = self._convert_graphql_input_to_dict(x, fields_to_check)
                d[active_flag_name] = True
                exists_in_db = self._is_object_in_db(mutation_class, context, d, info, *args, **kwargs)
                if exists_in_db:
                    object_to_remove = self._get_object_from_db(
                        mutation_class=mutation_class,
                        context=context,
                        data=d,
                        info=info,
                        *args,
                        **kwargs
                    )
                    removed = self._remove_association_between_models_from_db(
                        mutation_class=mutation_class,
                        context=context,
                        object_to_remove=object_to_remove,
                        data=d,
                        info=info,
                        *args,
                        **kwargs
                    )
                    elements_removed.extend(removed)

                else:
                    if not context.ignore_if_not_present:
                        raise GraphQLAppError(error_codes.OBJECT_NOT_FOUND, object=context.django_secondary_owner_type.__name__, values=d)

            new_len = self._get_number_of_elements_in_association(
                context=context
            )
            old_len = new_len + len(elements_removed)

            # yield result
            return mutation_class(**{
                output_name: elements_removed,
                old_length_output_name: old_len,
                new_length_output_name: new_len
            })

        # arguments
        arguments = dict()
        arguments[input_name] = self._get_remove_mutation_primary_input_list(
            context=context
        )
        arguments = self._configure_remove_mutation_inputs(arguments, context)
        return_value = self._get_remove_mutation_primary_output_list(context)

        return GraphQLHelper.create_mutation(
            mutation_class_name=str(mutation_class_name),
            description=description,
            arguments=arguments,
            return_type={
                output_name: return_value,
                old_length_output_name: GraphQLHelper.returns_required_int(
                    description=f"The number of elements in the collection before the remove operation was performed"),
                new_length_output_name: GraphQLHelper.returns_required_int(
                    description=f"The number of elements in the collection after the remove operation has been performed"),
            },
            body=body
        )


class RemoveByIds:
    """
    A class supporting a IAddRemoveElementGraphql.
    Use it if you want that the remove mutation accepts and yields ids of the models to remove from the associations
    """

    def _get_remove_mutation_primary_input_list(self, context: RemoveMutationContext) -> graphene.Field:
        """
        :return: an element that will belong to the mutation remove graphql input parameters. This
            element contains the list of elements to remove from the association
        """
        return GraphQLHelper.argument_required_id_list(
            entity=graphene.ID,
            description=f"The ids of the objects in the association {context.relation_name} to be removed"
        )

    def _get_remove_mutation_primary_output_list(self, context: RemoveMutationContext) -> graphene.Field:
        """
        :return: a list of elements that will be returned from the outptu of the mutation.
            It can be whatever you want
        """
        return GraphQLHelper.returns_nonnull_list(
            return_type=graphene.ID,
            description=f"the {context.django_secondary_owner_type.__name__} that we have just removed from the relation"
        )


class SimpleAddRemoveElementGraphQL(RemoveByIds, IAddRemoveElementGraphql):
    """
    A IAddRemoveElementGraphql that manage a N-N relationship.
    The remove mutation works by using ids
    """

    def __init__(self, relationship_manager: str):
        """
        :param relationship_manager: the name of the field in a N-N relationship endpoint **owning** the relationship
            repersenting the manager that manages the relationship
        """
        self.relationship_manager = relationship_manager

    def _is_object_in_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext], data: Dict[str, any], info: any,
                                *args, **kwargs) -> bool:
        return context.django_secondary_owner_type._default_manager.filter(**data).count() > 0

    def _add_object_to_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext],
                          data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        return context.django_secondary_owner_type._default_manager.create(**data)

    def _get_object_from_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext],
                          data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        return context.django_secondary_owner_type._default_manager.get(**data)

    def _get_number_of_elements_in_association(self, context: Union[AddMutationContext, RemoveMutationContext]) -> int:
        return getattr(context.django_main_owner_type, self.relationship_manager).all().count()

    def _add_association_between_models_in_db(self, context: Union[AddMutationContext, RemoveMutationContext],
                                              object_to_add: any) -> int:
        getattr(context.django_main_owner_type, self.relationship_manager).add(object_to_add)
        return 1

    def _remove_association_between_models_from_db(self, mutation_class: type, context: Union[AddMutationContext, RemoveMutationContext], data: Dict[str, any], info, *args,
                                                   **kwargs) -> List[any]:
        getattr(context.django_main_owner_type, self.relationship_manager).filter(**data).update(**{context.active_flag_name: False})
        return [1]



