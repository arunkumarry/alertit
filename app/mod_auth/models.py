from bson.objectid import ObjectId
from bson.json_util import dumps
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['themonbot']

class Mongo:

    # Insert a single document into a database
    def insert_one(self, data, coll_name):
        coll = db[coll_name]
        result = coll.insert_one(data)
        if result.acknowledged:
            return str(result.inserted_id)
        return None

    # Insert one or more document into a database
    def insert_many(self, data, coll_name):
        coll = db[coll_name]
        result = coll.insert_many(data)
        if result.acknowledged:
            return result.acknowledged
        return None

    # Find a single document from a database based on cond (internal)
    def find_one_internal(self, data, coll_name):
        coll = db[coll_name]
        result = coll.find_one(data)
        if result:
            result['_id'] = (result['_id'])
            return result
        else:
            return result

    # Find a single document from a database based on cond (external)
    def find_one(self, data, coll_name):
        coll = db[coll_name]
        result = coll.find_one(data)
        if result:
            result['_id'] = str(result['_id'])
            return dumps(result)
        else:
            return dumps(result)

    # Find all documents from a database
    def find(self, coll_name):
        coll = db[coll_name]
        arr = []
        for q in coll.find():
            dict = {}
            for a in q.keys():
                if isinstance(q[a], ObjectId):
                    dict[a] = str(q[a])
                else:
                    dict[a] = q[a]
            arr.append(dict)

        return dumps(arr)

    # Find the documents from a database which is min
    def find_min(self,  params, coll_name):
        coll = db[coll_name]
        arr = {}
        for doc in coll.find().sort(params,1).limit(1):
           arr = doc

        return arr

    # Find all documents from a database based on condition
    def find_cond(self, data, coll_name):
       coll = db[coll_name]
       arr = []
       for q in coll.find(data):
           dict = {}
           for a in q.keys():
               if isinstance(q[a], ObjectId):
                   dict[a] = str(q[a])
               else:
                   dict[a] = q[a]
           arr.append(dict)

       return arr

    # Delete a document from a database
    def delete_one(self, id, coll_name):
        coll = db[coll_name]
        result = coll.remove({'_id': ObjectId(id)})
        if str(result):
            return result
        else:
            return None

    # updates the instances in the database
    def update_instance(self, data, coll_name):
        coll = db[coll_name]
        removed_id = data.pop('user_id',None)
        result = coll.update({'user_id': ObjectId(removed_id)}, {'$inc': {"instance_counter":1}})
        if result:
            return result
        else:
            return None

    # Returns doc prior to updation
    def update_one(self, data, coll_name):
        coll = db[coll_name]
        removed_id = data.pop('_id', None)
        result = coll.update_one({'_id': ObjectId(removed_id)}, {'$set': data})
        if result:
            return result.acknowledged
        else:
            return None

    # Returns doc prior to updation
    def update(self, coll_name):
        coll = db[coll_name]
        result = coll.update({}, {'$set': {"instance_counter":0}},multi=True)
        if result:
            return result
        else:
            return None

    # Returns the number of documents in a collection
    def count(self, coll_name):
        coll = db[coll_name]
        count = coll.count()
        return count
