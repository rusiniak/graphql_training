from graphene import Schema, ObjectType, String, Int, Field, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}
        Query.users.append(user)
        return CreateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id):
        removed_user = None
        for user in Query.users:
            if user["id"] == user_id:
                removed_user = user
                Query.users.remove(user)
        return DeleteUser(user=removed_user) if removed_user else None

class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for a_user in Query.users:
            if a_user["id"] == user_id:
                user = a_user
                break
        if not user:
            return None
        if name is not None:
            user["name"] = name
        if age is not None:
            user["age"] = age
        return UpdateUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = List(UserType, min_age=Int())

    users = [
        {"id": 1, "name": "Mariusz Rusiniak", "age": 38},
        {"id": 2, "name": "Marcin Rusiniak", "age": 37},
        {"id": 3, "name": "Marta Rusiniak", "age": 34},
        {"id": 4, "name": "Kasia Rusiniak", "age": 32},
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

gql = '''
mutation{
    createUser(name: "New User", age: 100) {
        user {
            id
            name
            age
        }
    }
}
'''

gql2 = '''
query{
    user(userId: 1) {
            id
            name
            age
    }
}
'''

gql_update = '''
mutation{
    updateUser(userId: 1, name: "New User", age: 100) {
        user {
            id
            name
            age
        }
    }
}
'''
gql_delete = '''
mutation{
    deleteUser(userId: 1) {
        user {
            id
            name
            age
        }
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql_delete)
    print(result)
    result = schema.execute(gql2)
    print(result)
