from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

graph = GraphDatabase.driver('neo4j+s://1baf8087.databases.neo4j.io', auth=('neo4j', 'GHvoYzAKuJrA88v8eDuoYhfZ3538urq-07A_0OCcz-I'))


def execute(query):
    with graph.session(database="neo4j") as session:
        return session.run(query)


class Person:
    def __init__(self, name):
        self.name = name

    def find(self):
        query = "MATCH (n:Person {name: '" + self.name + "'}) RETURN n"
        result = execute(query)
        return result

    def add(self):
        # if not self.find():
        query = "CREATE(n:Person {name:'" + self.name + "'})"
        execute(query)
        return True
        # else:
        #     return False