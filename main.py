from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db = mysql.connector.connect(
    host="roundhouse.proxy.rlwy.net",
    port=41164,
    user="root",
    password="zzRogpFIBEJhCwrmpZgxeWZHphcnnrIQ",
    database="railway"
)

# Crear un cursor para la interacción con la base de datos
cursor = db.cursor(dictionary=True)

# CRUD de productos
@app.route('/productos', methods=['POST'])
def create_producto():
    data = request.json
    cursor.execute("INSERT INTO Producto (CodigoProducto, Nombre, Marca) VALUES (%s, %s, %s)",
                   (data['CodigoProducto'], data['Nombre'], data['Marca']))
    db.commit()
    return jsonify({'message': 'Producto creado'}), 201

@app.route('/productos', methods=['GET'])
def get_productos():
    cursor.execute("""
        SELECT 
            p.CodigoProducto,
            p.Nombre,
            p.Marca,
            d.Detalles,
            d.Categoria,
            i.Cantidad,
            i.Precio
        FROM 
            Producto p
        LEFT JOIN 
            Descripcion d ON p.CodigoProducto = d.CodigoProducto
        LEFT JOIN 
            Inventario i ON p.CodigoProducto = i.CodigoProducto""")
    productos = cursor.fetchall()
    return jsonify(productos)

@app.route('/productos/<int:codigo>', methods=['GET'])
def get_producto(codigo):
    cursor.execute("""
        SELECT 
            p.CodigoProducto,
            p.Nombre,
            p.Marca,
            d.Detalles,
            d.Categoria,
            i.Cantidad,
            i.Precio
        FROM 
            Producto p
        LEFT JOIN 
            Descripcion d ON p.CodigoProducto = d.CodigoProducto
        LEFT JOIN 
            Inventario i ON p.CodigoProducto = i.CodigoProducto
        WHERE 
            p.CodigoProducto = %s
    """, (codigo,))
    producto = cursor.fetchone()
    return jsonify(producto)

@app.route('/productos/<int:codigo>', methods=['PUT'])
def update_producto(codigo):
    data = request.json
    cursor.execute("UPDATE Producto SET Nombre = %s, Marca = %s WHERE CodigoProducto = %s",
                   (data['Nombre'], data['Marca'], codigo))
    db.commit()
    return jsonify({'message': 'Producto actualizado'})

@app.route('/productos/<int:codigo>', methods=['DELETE'])
def delete_producto(codigo):
    try:
        # Eliminar inventario relacionado con el producto
        cursor.execute("DELETE FROM Inventario WHERE CodigoProducto = %s", (codigo,))
        # Eliminar descripciones relacionadas con el producto
        cursor.execute("DELETE FROM Descripcion WHERE CodigoProducto = %s", (codigo,))
        # Eliminar el producto
        cursor.execute("DELETE FROM Producto WHERE CodigoProducto = %s", (codigo,))
        db.commit()
        return jsonify({'message': 'Producto eliminado'})
    except mysql.connector.Error as err:
        db.rollback()
        return jsonify({'error': str(err)}), 500


# CRUD de descripciones
@app.route('/descripciones', methods=['POST'])
def create_descripcion():
    data = request.json
    cursor.execute("INSERT INTO Descripcion (IdDescripcion, CodigoProducto, Detalles, Categoria) VALUES (%s, %s, %s, %s)",
                   (data['IdDescripcion'], data['CodigoProducto'], data['Detalles'], data['Categoria']))
    db.commit()
    return jsonify({'message': 'Descripción creada'}), 201

@app.route('/descripciones/<int:id>', methods=['PUT'])
def update_descripcion(id):
    data = request.json
    cursor.execute("UPDATE Descripcion SET CodigoProducto = %s, Detalles = %s, Categoria = %s WHERE IdDescripcion = %s",
                   (data['CodigoProducto'], data['Detalles'], data['Categoria'], id))
    db.commit()
    return jsonify({'message': 'Descripción actualizada'})



# CRUD de inventarios
@app.route('/inventarios', methods=['POST'])
def create_inventario():
    data = request.json
    cursor.execute("INSERT INTO Inventario (IdInventario, CodigoProducto, Cantidad, Precio) VALUES (%s, %s, %s, %s)",
                   (data['IdInventario'], data['CodigoProducto'], data['Cantidad'], data['Precio']))
    db.commit()
    return jsonify({'message': 'Inventario creado'}), 201

@app.route('/inventarios/<int:id>', methods=['PUT'])
def update_inventario(id):
    data = request.json
    cursor.execute("UPDATE Inventario SET CodigoProducto = %s, Cantidad = %s, Precio = %s WHERE IdInventario = %s",
                   (data['CodigoProducto'], data['Cantidad'], data['Precio'], id))
    db.commit()
    return jsonify({'message': 'Inventario actualizado'})



if __name__ == '__main__':
    app.run(debug=True)
