from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

graph = GraphDatabase.driver('neo4j+s://1baf8087.databases.neo4j.io', auth=('neo4j', 'GHvoYzAKuJrA88v8eDuoYhfZ3538urq-07A_0OCcz-I'))

# simple function to wrap running query
def execute(query):
    with graph.session(database="neo4j") as session:
        return session.run(query)


class Person:
    def __init__(self, name):
        self.name = name

    # def find(self):
    #     query = "MATCH (n:Person {name: '" + self.name + "'}) RETURN n"
    #     result = execute(query)
    #     print([row["name"] for row in result])
    #     # if len(result.) > 0:
    #     return [row["name"] for row in result]
    #     # return False
    #
    # def add(self):
    #     print("-----")
    #     print(self.find())
    #     print(self.name)
    #     # if not self.find():
    #     # print(self.find().data().count().)
    #     query = "CREATE(n:Person {name:'" + self.name + "'})"
    #     execute(query)
    #     return True
    #     # else:
    #     #     return False

    def find(self):
        with graph.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, self.name)
            return result

    @staticmethod
    def _find_and_return_person(tx, name):
        query = (
            "MATCH (p:Person) "
            "WHERE p.name = $name "
            "RETURN p.name AS name"
        )
        result = tx.run(query, name=name)
        return [row["name"] for row in result]

    def add(self):
        if not self.find():
            query = "CREATE(n:Person {name:'" + self.name + "'})"
            execute(query)
            return True
        else:
            return False

    def delete(self):
        if not self.find():
            return False
        else:
            query = "MATCH (p:Person {name: '" + self.name + "'}) DETACH DELETE p "
            execute(query)
            return True

class Location:
    def __init__(self, city, state):
        self.city = city
        self.state = state

def list_all_people():
    with graph.session(database="neo4j") as session:
        return session.execute_read(query_all_people)

def query_all_people(tx):
    query = "MATCH (p:Person) RETURN p.name AS name"
    result = tx.run(query)
    return [row["name"] for row in result]

def query_all_locations(tx):
    query = "MATCH (n:Location) RETURN (n)"
    result = tx.run(query)
    return [dict(row[0]) for row in result]
def list_all_locations():
    with graph.session(database="neo4j") as session:
        return session.execute_read(query_all_locations)