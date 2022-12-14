from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

graph = GraphDatabase.driver('neo4j+s://a4565860.databases.neo4j.io', auth=('neo4j', 'C7pmAvK6mg12fPB7frIUUQksvuOWAJ8nutIBwzmT7aQ'))

# simple function to wrap running query
def execute(query):
    with graph.session(database="neo4j") as session:
        return session.run(query)

# def create_node(tx, query):
#     tx.run(query)

def qr_plain(tx, query):
    result = tx.run(query)
    return result

def qr(tx, query):
    result = tx.run(query)
    return [dict(row) for row in result]


def execute_query(query):
    with graph.session(database="neo4j") as session:
        return session.execute_read(qr, query)

class Person:
    def __init__(self, name):
        self.name = name

    def find(self):
        with graph.session(database="neo4j") as session:
            result = session.execute_read(self._find_and_return_person, self.name)
            return result

    @staticmethod
    def _find_and_return_person(tx, name):
        query = "MATCH (n:Person {name: '" + name + "'}) RETURN n"
        result = tx.run(query)
        return [dict(row) for row in result]

    def add(self):
        if not self.find():
            query = "CREATE(n:Person {name:'" + self.name + "'})"
            # session = graph.session()
            # session.execute_write(create_node(query))
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

    ### relations management
    def add_friend(self, person):
        if self.find() and person.find():
            query = "MATCH(a:Person {name:'" + self.name + "'}),(b:Person {name:'" + person.name + "'}) MERGE(a)-[r:FRIENDS]->(b) RETURN a,b"
            execute(query)
            return True
        else:
            return False

    def get_friends(self):
        query = "OPTIONAL MATCH (a:Person {name:'" + self.name + "'})-[r:FRIENDS]-(b:Person) RETURN b"
        result = execute_query(query)
        return result

    def add_birthplace(self, place):
        if self.find() and place.find():
            query = "MATCH(a:Person {name:'" + self.name + "'}),(b:Location {city:'" + place.city + "', state:'" + place.state + "'}) MERGE(a)-[r:LIVE_IN]->(b) RETURN a,b"
            execute(query)
            return True
        else:
            return False

    def get_birthplace(self):
        query = "OPTIONAL MATCH (a:Person {name:'" + self.name + "'})-[r:LIVE_IN]-(b:Location) RETURN b"
        # with graph.session(database="neo4j") as session:
        #     result = session.read_transaction(qr_plain, query)
        # print([dict(row) for row in result])
        result = execute_query(query)
        print(result)
        return result
        # return [dict(row) for row in result]

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
            return result

    def get_people_live_in(self, city):
        query = "OPTIONAL MATCH (a:Person)-[r:LIVE_IN]-(b:Location {city:'" + self.city + "'}) RETURN a.name as name, b.city as city"
        result = execute_query(query)
        return result


def list_all_people():
    with graph.session(database="neo4j") as session:
        return session.execute_read(query_all_people)


def query_all_people(tx):
    query = "MATCH (p:Person) RETURN p.name AS name"
    result = tx.run(query)
    return [dict(row) for row in result]


def query_all_locations(tx):
    query = "MATCH (n:Location) RETURN (n)"
    result = tx.run(query)
    return [dict(row[0]) for row in result]

def list_all_locations():
    with graph.session(database="neo4j") as session:
        return session.execute_read(query_all_locations)