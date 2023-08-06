import abc
from typing import Dict, Optional, List, Tuple

import stringcase
from graphene import Field

from django_koldar_utils.django import django_helpers
from django_koldar_utils.graphql import error_codes, graphene
from django_koldar_utils.graphql.GraphQLAppError import GraphQLAppError
from django_koldar_utils.graphql.GraphQLHelper import GraphQLHelper


class IAddRemoveElementGraphql(abc.ABC):
    """
    A class that generates classes representing graphql queries adding adn removing items from a relationship.
    Relationship can
    """

    @abc.abstractmethod
    def _is_element_in_callable(self, mutation_class: type, django_element_type: type, data: Dict[str, any], info: any,
                                *args, **kwargs) -> bool:
        """
        Check if an object passed in input to the add/remove mutation is already present or not.
        By default we will check if there exists a row with the exact match of data

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
    def _add_or_get_object_to_db(self, mutation_class: type, django_element_type: type, already_present: bool,
                          data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        """
        Add an object passed in input to the database.
        By default we will call create with data

        :param mutation_class: mutation class that we are building
        :param django_element_type: django element, passed from generate
        :param already_present: true if the object si present in the database, false otherwise
        :param data: set of input parameters fo the graphql mutation
        :param info: graphql info
        :param args: graphql args
        :param kwargs: graphql kwargs
        :return: true if the object is already present in the database, false otherwise.
        """
        pass

    @abc.abstractmethod
    def _get_element_to_be_removed(self, mutation_class: type, django_element_type: type, active_flag_name: str,
                          data: Dict[str, any], info, *args, **kwargs) -> any:
        """
        Fetch the element that we need to be removed from the association involved

        :return: an object that will be passed as-is to _remove_association_between_models_from_db
        """
        pass

    @abc.abstractmethod
    def _get_number_of_elements_in_association(self, django_element_type: type, django_list_owner_type: type) -> int:
        """
        :param django_element_type: element in the relation to remove
        :param django_list_owner_type: model containing a list repersenting the association.
        :return: number of elements in the given association
        """
        pass

    @abc.abstractmethod
    def _add_association_between_models_in_db(self, django_element_type: type, django_list_owner_type: type, object_to_add: any) -> int:
        """
        :return: number of elements added in the association
        """
        pass

    @abc.abstractmethod
    def _remove_association_between_models_from_db(self, mutation_class: type, django_element_type: type, django_list_owner_type: type, active_flag_name: str,
                          data: Dict[str, any], info, *args, **kwargs) -> List[any]:
        """
        Concretely remove the association of a given relationship

        :return: a list of elements removed from the association. You can return whatever you want. The concatenation
        of these values will be returned from this mutation
        """
        pass

    @abc.abstractmethod
    def _get_remove_mutation_primary_input_list(self, graphene_element_input_type: type,
                                                relation_name: str) -> graphene.Field:
        """
        :return: an element that will belong to the mutation remove graphql input parameters. This
            element contains the list of elements to remove from the association
        """
        pass

    @abc.abstractmethod
    def _get_remove_mutation_primary_output_list(self, django_element_type: type) -> graphene.Field:
        """
        :return: a list of elements that will be returned from the outptu of the mutation.
            It can be whatever you want
        """
        pass

    def models_active_flag_name(self, django_element_type: type) -> str:
        """
        :param django_element_type: class repersenting the model
        :return: name of the flag that represents whether or not the row should be considered or not
        """
        return "active"

    def get_add_mutation_input_parameter_name(self, django_element_type: type, graphene_element_input_type: type) -> str:
        """
        :return: name of the graphql mutation parameter representing the object to add
        """
        return "item"

    def get_add_mutation_output_return_value_name(self, django_element_type: type, graphene_element_input_type: type,
                                     relation_name: str) -> str:
        """
        :return: name of the return value of the add mutation
        """
        return f"{relation_name}AddOutcome"

    def get_fields_to_check(self, django_element_type: type, graphene_element_input_type, relation_name: str) -> List[
        Field]:
        """
        :return: parameters in the graphql mutation input parameter representing unique fields. Useful for checking if
            a value has already been added to the database
        """
        return list(django_helpers.get_unique_field_names(django_element_type))

    def get_old_length_output_name(self, django_element_type: type, graphene_element_input_type: type,
                                   relation_name: str) -> str:
        return f"{relation_name}OldLength"

    def new_length_output_name(self, django_element_type: type, graphene_element_input_type: type,
                               relation_name: str) -> str:
        return f"{relation_name}NewLength"

    def added_output_name(self, django_element_type: type, graphene_element_input_type: type,
                          relation_name: str) -> str:
        return f"{relation_name}Added"

    def created_output_name(self, django_element_type: type, graphene_element_input_type: type,
                            relation_name: str) -> str:
        return f"{relation_name}Created"

    def generate(self, django_list_owner_type: type, django_element_type: type,
                 graphene_element_input_type: type, relation_name: str,
                 add_if_not_present: bool = False,
                 generate_add_mutation: bool = True,
                 generate_remove_mutation: bool = True,
                 ) -> Tuple[type, type]:
        """
        :param django_list_owner_type: django type owning a list of items of type django_element_owner_type
        :param django_element_type: django type of the array of list
        :param relation_name: name of the relationship represented by the list
        :param graphene_element_input_type: graphene type representing a single cell in the list owned by django_list_owner_type. The type represents a graphql input type.
        :param add_if_not_present: if this variable is set to True, if the user add a non persisteed django_element_type instance as the input of the mutation,
            we will first persist such an object
        :param generate_remove_mutation: if set, we will create a remove mutation
        :param generate_add_mutation: if set, we will create an add mutation
        :reutrn: first type representing this add element to list mutation, while the second represents the removal from this list
        """

        if generate_add_mutation:
            add_mutation = self._generate_add_mutation(
                django_list_owner_type=django_list_owner_type,
                django_element_type=django_element_type,
                graphene_element_input_type=graphene_element_input_type,
                relation_name=relation_name,
                add_if_not_present=add_if_not_present,
            )
        else:
            add_mutation = None

        if generate_remove_mutation:
            remove_mutation = None
        else:
            remove_mutation = None

        return add_mutation, remove_mutation

    def _generate_add_mutation(self,
                               django_list_owner_type: type, django_element_type: type,
                               graphene_element_input_type: type, relation_name: str,
                               add_if_not_present: bool = False,
                               ) -> type:

        description = self._get_add_mutation_description(
            django_element_type=django_element_type,
            django_list_owner_type=django_list_owner_type,
            relation_name=relation_name,
            add_if_not_present=add_if_not_present
        )
        active_flag_name = self.models_active_flag_name(django_element_type)
        input_name = self.get_add_mutation_input_parameter_name(django_element_type, graphene_element_input_type)
        output_name = self.get_add_mutation_output_return_value_name(django_element_type, graphene_element_input_type, relation_name)
        fields_to_check = self.get_fields_to_check(django_element_type, graphene_element_input_type, relation_name)
        old_length_output_name = self.get_old_length_output_name(django_element_type, graphene_element_input_type,
                                                                 relation_name)
        new_length_output_name = self.new_length_output_name(django_element_type, graphene_element_input_type,
                                                             relation_name)
        added_output_name = self.added_output_name(django_element_type, graphene_element_input_type, relation_name)
        created_output_name = self.created_output_name(django_element_type, graphene_element_input_type, relation_name)

        mutation_class_name = self._add_mutation_name(
            django_element_type=django_element_type,
            django_list_owner_type=django_list_owner_type,
            relation_name=relation_name
        )

        def body(mutation_class, info, *args, **kwargs) -> any:
            nonlocal self
            result_create = False

            input = kwargs[input_name]
            d = dict()
            for f in fields_to_check:
                d[f] = getattr(input, f)
            d[active_flag_name] = True
            # check if the element we need to add exists in the database
            if not self._is_element_in_callable(mutation_class, django_element_type, d, info, *args, **kwargs):
                if add_if_not_present:
                    # we need to create the object
                    # create argument and omits the None values
                    create_args = {k: v for k, v in dict(input).items() if v is not None}
                    object_to_add = self._add_or_get_object_to_db(mutation_class, django_element_type, False, create_args,
                                                           info, *args, **kwargs)
                    if object_to_add is None:
                        raise GraphQLAppError(error_codes.CREATION_FAILED, object=django_element_type.__name__,
                                              values=create_args)
                    result_create = True
                else:
                    raise GraphQLAppError(error_codes.OBJECT_NOT_FOUND, object=django_element_type.__name__, values=d)
            else:
                object_to_add = self._add_or_get_object_to_db(mutation_class, django_element_type, True, d, info, *args, **kwargs)

            # ok, now add the relationship (if needed)
            added = self._add_association_between_models_in_db(
                django_element_type=django_element_type,
                django_list_owner_type=django_list_owner_type,
                object_to_add=object_to_add
            )

            new_len = self._get_number_of_elements_in_association(
                django_element_type=django_element_type,
                django_list_owner_type=django_list_owner_type
            )
            old_len = new_len - added
            result_added = new_len > old_len

            # yield result
            return mutation_class(**{
                output_name: object_to_add,
                added_output_name: result_added,
                created_output_name: result_create,
                old_length_output_name: old_len,
                new_length_output_name: new_len
            })

        arguments = dict()
        arguments[input_name] = GraphQLHelper.argument_required_input(graphene_element_input_type,
                                                                      description="The object to add into the database. id should not be populated. ")

        arguments = self.configure_add_mutation_inputs(arguments, django_element_type)

        return GraphQLHelper.create_mutation(
            mutation_class_name=str(mutation_class_name),
            description=description,
            arguments=arguments,
            return_type={
                output_name: GraphQLHelper.returns_nonnull(django_element_type,
                                                           description=f"the {django_element_type.__name__} we just added in the relation"),
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

    def configure_add_mutation_inputs(self, original_arguments: Dict[str, Field], django_element_type: type) -> Dict[
        str, Field]:
        return original_arguments

    def configure_remove_mutation_inputs(self, original_arguments: Dict[str, Field], django_element_type: type) -> Dict[
        str, Field]:
        return original_arguments

    def _get_add_mutation_description(self, django_element_type: type, django_list_owner_type: type,
                                      add_if_not_present: bool, relation_name: str) -> str:
        if add_if_not_present:
            not_present = "We will persist it first by creating the object"
        else:
            not_present = "We will raise exception"
        dsc = f"""Allows to add a new element of type {django_element_type.__name__} to the list owned
            by class {django_list_owner_type.__name__} associated with the relation \"{relation_name}\". If an element
            is already within such a list we do nothing. If the element input is not already persisted in the database (i.e., the input has an id not null), {not_present}. 
            If the item to add has the active flag set to False, we do nothing. 
            The function returns the element added in the relationship as well as the previous and after length of the collection w.r.t. the add operation.
            We will also return whether or not we actually have added the new item to the collection and if we had to first create a new item
            in the database.
            """
        return dsc

    def _get_remove_mutation_description(self, django_element_type: type, django_list_owner_type: type,
                                      ignore_if_not_present: bool, relation_name: str) -> str:
        if ignore_if_not_present:
            not_present = "we will do nothing"
        else:
            not_present = "we will raise exception"
        dsc = f"""Allows to remove a relationship between 2 objects previously created. The relationship involved 
            element of type {django_element_type.__name__} to the list owned
            by class {django_list_owner_type.__name__} associated with the relation \"{relation_name}\". If we are 
            requested to remove an element which is not in the list, {not_present}. 
            If the item to remove exists and has the active flag set to False, we do nothing. 
            The function returns the element added in the relationship as well as the previous and after length of the collection w.r.t. the remove operation.
            We will also return whether or not we actually have removed the item to the collection.
            With this mutation you can remove multiple items in one sweep.
            """
        return dsc

    def get_remove_mutation_input_parameter_name(self, django_element_type: type, graphene_element_input_type: type) -> str:
        """
        :return: name of the graphql mutation parameter representing the object to add
        """
        return "itemsToRemove"

    def get_remove_mutation_output_return_value_name(self, django_element_type: type, graphene_element_input_type: type,
                                     relation_name: str) -> str:
        """
        :return: name of the return value of the add mutation
        """
        return f"{stringcase.camelcase(relation_name)}RemoveOutcome"

    def _add_mutation_name(self, django_element_type: type, django_list_owner_type: type, relation_name: str) -> str:
        """
        Generate the name of the class representing the add mutation
        """
        return f"Add{django_element_type.__name__}To{stringcase.pascalcase(relation_name)}Of{django_list_owner_type.__name__}"

    def _remove_mutation_name(self, django_element_type: type, django_list_owner_type: type, relation_name: str) -> str:
        """
        Generate the name of the class representing the add mutation
        """
        return f"Remove{django_element_type.__name__}From{stringcase.pascalcase(relation_name)}Of{django_list_owner_type.__name__}"

    def _generate_remove_mutation(self,
                               django_list_owner_type: type, django_element_type: type,
                               graphene_element_input_type: type, relation_name: str,
                               ignore_if_not_present: bool = False,
                               ) -> type:

        description = self._get_remove_mutation_description(
            django_element_type=django_element_type,
            django_list_owner_type=django_list_owner_type,
            relation_name=relation_name,
            ignore_if_not_present=ignore_if_not_present
        )
        active_flag_name = self.models_active_flag_name(django_element_type)
        input_name = self.get_remove_mutation_input_parameter_name(django_element_type, graphene_element_input_type)
        output_name = self.get_remove_mutation_output_return_value_name(django_element_type, graphene_element_input_type, relation_name)
        fields_to_check = self.get_fields_to_check(django_element_type, graphene_element_input_type, relation_name)
        old_length_output_name = self.get_old_length_output_name(django_element_type, graphene_element_input_type,
                                                                 relation_name)
        new_length_output_name = self.new_length_output_name(django_element_type, graphene_element_input_type,
                                                             relation_name)

        mutation_class_name = self._remove_mutation_name(
            django_element_type=django_element_type,
            django_list_owner_type=django_list_owner_type,
            relation_name=relation_name
        )

        def body(mutation_class, info, *args, **kwargs) -> any:
            nonlocal self
            result_create = False

            # input parameter is a list
            input_parameter = kwargs[input_name]
            # for every element in the list "input_parameter", we try to remove it
            elements_removed = []
            for x in input_parameter:
                d = dict()
                for f in fields_to_check:
                    d[f] = getattr(x, f)
                d[active_flag_name] = True
                exists_in_db = self._is_element_in_callable(mutation_class, django_element_type, d, info, *args, **kwargs)
                if exists_in_db:
                    object_to_remove = self._get_element_to_be_removed(
                        mutation_class=mutation_class,
                        django_element_type=django_element_type,
                        active_flag_name=active_flag_name,
                        data=d,
                        info=info,
                        *args,
                        **kwargs
                    )
                    removed = self._remove_association_between_models_from_db(
                        mutation_class=mutation_class,
                        django_element_type=django_element_type,
                        active_flag_name=active_flag_name,
                        object_to_remove=object_to_remove,
                        data=d,
                        info=info,
                        *args,
                        **kwargs
                    )
                    elements_removed.extend(removed)

                else:
                    if not ignore_if_not_present:
                        raise GraphQLAppError(error_codes.OBJECT_NOT_FOUND, object=django_element_type.__name__, values=d)

            new_len = self._get_number_of_elements_in_association(
                django_element_type=django_element_type,
                django_list_owner_type=django_list_owner_type,
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
        arguments[input_name] = self._get_remove_mutation_primary_input_list(graphene_element_input_type)
        arguments = self.configure_remove_mutation_inputs(arguments, django_element_type)
        return_value = self._get_remove_mutation_primary_output_list(django_element_type)

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

    def _get_remove_mutation_primary_input_list(self, graphene_element_input_type: type,
                                                relation_name: str) -> graphene.Field:
        """
        :return: an element that will belong to the mutation remove graphql input parameters. This
            element contains the list of elements to remove from the association
        """
        return GraphQLHelper.returns_nonnull_list(
            return_type=graphene_element_input_type,
            description=f"The ids of the objects in the association {relation_name} to be removed"
        )


    def _get_remove_mutation_primary_output_list(self, django_element_type: type) -> graphene.Field:
        """
        :return: a list of elements that will be returned from the outptu of the mutation.
            It can be whatever you want
        """
        return GraphQLHelper.returns_nonnull_list(
            return_type=graphene.ID,
            description=f"the {django_element_type.__name__} that we have just removed from the relation"
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

    def _is_element_in_callable(self, mutation_class: type, django_element_type: type, data: Dict[str, any], info: any,
                                *args, **kwargs) -> bool:
        return django_element_type._default_manager.filter(**data) is not None

    def _add_or_get_object_to_db(self, mutation_class: type, django_element_type: type, already_present: bool,
                                 data: Dict[str, any], info, *args, **kwargs) -> Optional[any]:
        if already_present:
            return django_element_type._default_manager.get(**data)
        else:
            return django_element_type._default_manager.create(**data)

    def _get_element_to_be_removed(self, mutation_class: type, django_element_type: type, active_flag_name: str,
                                   data: Dict[str, any], info, *args, **kwargs) -> any:
        return django_element_type._default_manager.get(**data)

    def _get_number_of_elements_in_association(self, django_element_type: type, django_list_owner_type: type) -> int:
        return getattr(django_list_owner_type, self.relationship_manager).all().count()

    def _add_association_between_models_in_db(self, django_element_type: type, django_list_owner_type: type,
                                              object_to_add: any) -> int:
        getattr(django_list_owner_type, self.relationship_manager).add(object_to_add)
        return 1

    def _remove_association_between_models_from_db(self, mutation_class: type, django_element_type: type, django_list_owner_type: type,
                                                   active_flag_name: str, data: Dict[str, any], info, *args,
                                                   **kwargs) -> List[any]:
        getattr(django_list_owner_type, self.relationship_manager).filter(**data).update(**{active_flag_name: False})
        return [1]