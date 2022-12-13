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

    def find(self):
        with graph.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, self.name)
            return result

    @staticmethod
    def _find_and_return_person(tx, name):
        query = "CREATE(n:Person {name:'" + name + "'})"
        result = tx.run(query)
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

    @staticmethod
    def _read_wrapper(tx, query):
        result = tx.run(query)
        return [dict(row) for row in result]

    def find(self):
        with graph.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_location, self.city, self.state)
            return result
    @staticmethod
    def _find_and_return_location(tx, city, state):
        query = "MATCH (n:Location {city:'" + city + "', state:'" + state + "'}) RETURN n"
        result = tx.run(query)
        return [dict(row[0]) for row in result]

    def add(self):
        if not self.find():
            query = "CREATE (n:Location {city:'" + self.city + "', state:'" + self.state + "'}) RETURN n"
            execute(query)
            return True
        else:
            return False

    def delete(self):
        if not self.find():
            return False
        else:
            query = "MATCH (n:Location {city:'" + self.city + "', state:'" + self.state + "'}) DETACH DELETE n"
            execute(query)
            return True

    def add_dist(self, city2, dist):
        query = "MATCH (a:Location {city: '" + self.city + "', state: '" + self.state + "'}),(b:Location {city: '" + city2.city + "', state: '" + city2.state + "'}) MERGE(a)-[r:DIST {dist: '" + dist +"'}]->(b) RETURN a,b"
        result = execute(query)
        return result

    @staticmethod
    def _find_and_return_distance(tx, query):
        result = tx.run(query)
        return [[row["city"], row["relations"]] for row in result]
    def get_dist(self):
        query = "OPTIONAL MATCH a= (Location {city: '" + self.city + "', state: '" + self.state + "'}) -[:DIST]-(city) RETURN relationships(a) as relations, city.city as city"
        with graph.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_distance, query)
            for elem in result:
                print(elem)
            return result


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