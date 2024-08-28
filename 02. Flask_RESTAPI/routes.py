from flask import Flask, request, jsonify, abort
from database import get_db
import crud

def register_routes(app: Flask):
  @app.route('/items', methods=['POST'])
  def create_item_route():
    db = next(get_db())
    data = request.get_json() # 유저가 보낸 데이터
    print("유저가 보낸 데이터: ", data)
    new_item = crud.create_item(db, data['name'], data['price'], data['stock']) # circular import

    return jsonify({
      'id':new_item.id,
      'name':new_item.name,
      'price':new_item.price,
      'stock':new_item.stock,
      'created_at':new_item.created_at.isoformat()
    }), 201

  @app.route('/items/<int:item_id>', methods=['GET'])
  def get_item_route(item_id):
    db = next(get_db())
    item = crud.get_item(db, item_id)

    if item is None:
      abort(404)
    return jsonify({
      'id':item.id,
      'name':item.name,
      'price':item.price,
      'stock':item.stock,
      'created_at':item.created_at.isoformat()
    }), 200

  @app.route('/items', methods=['GET'])
  def get_all_items_route():
    db = next(get_db())
    items = crud.get_all_items(db)

    return jsonify([{
      'id':new_item.id,
      'name':new_item.name,
      'price':new_item.price,
      'stock':new_item.stock,
      'created_at':new_item.created_at.isoformat()
    } for new_item in items]), 201
  
  @app.route('/items/<int:item_id>', methods=['PUT'])
  def update_item_route(item_id):
    db = next(get_db())
    data = request.get_json()

    updated_item = crud.update_item(
      db=db,
      item_id=item_id,
      name=data['name'],
      price=data['price'],
      stock=data['stock']
    )

    if updated_item is None:
      abort(404)

    return {"message":f"Successfully updated item (Item Id: {item_id})"}
  
  @app.route('/items/<int:item_id>', methods=['DELETE'])
  def delete_item_route(item_id):
    db = next(get_db())

    deleted_item = crud.delete_item(db=db, item_id=item_id)

    if deleted_item is None:
      abort(404)
    return {"message":f"Successfully deleted item (Item Id: {item_id})"}

  # + LLM 챗팅