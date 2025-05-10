from flask import Flask, jsonify, request

app = Flask(__name__)

items=[
    {"id":1,"nome":"item 1", "preco":10.0},
    {"id":2,"nome":"item 2", "preco":20.0},
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items),200

@app.route('/items/<int:item_id>',methods=['GET'])
def get_item(item_id):
    item= next((item for item in items if item["id"]== item_id), None)
    if item:
        return jsonify(item),200
    else:
        return jsonify({"erro": "item nao encontado"}), 404

@app.route('/items', methods=['POST'])

def create_item():
    data= request.json
    new_item= {
        "id": len(items)+1,
        "nome": data["nome"],
        "preco": data ["preco"]
    }

    items.append(new_item)
    return jsonify(new_item),201

@app.route('/items/<int:item_id>',methods =['PUT'])
def update_item(item_id):
    data =request.json
    item= next((item for item in items if item["id"]==item_id),None)
    if item:
        item["nome"] = data["nome"]
        item["preco"] = data["preco"]
        return jsonify(item),200
    else:
        return jsonify({"error":"not found"}),404
    
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items= [item for item in items if item ["id"] != item_id]
    return jsonify({"message":"deleted!"}),200

if __name__ == '__main__':
    app.run(debug=True)