from flask import Flask, render_template, request, redirect, url_for, flash
from varasto import Varasto

app = Flask(__name__)
# SECURITY WARNING: Change this secret key in production!
# Use environment variables: app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = 'dev-secret-key-change-in-production'

# In-memory storage for warehouses
warehouses = {}
warehouse_counter = 0


@app.route('/')
def index():
    """Display all warehouses."""
    return render_template('index.html', warehouses=warehouses)


@app.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """Create a new warehouse."""
    if request.method == 'POST':
        global warehouse_counter
        name = request.form.get('name', '').strip()
        try:
            capacity = float(request.form.get('capacity', 0))
            initial_stock = float(request.form.get('initial_stock', 0))

            if not name:
                flash('Warehouse name is required', 'error')
                return redirect(url_for('create_warehouse'))

            if capacity <= 0:
                flash('Capacity must be greater than 0', 'error')
                return redirect(url_for('create_warehouse'))

            warehouse_counter += 1
            warehouses[warehouse_counter] = {
                'id': warehouse_counter,
                'name': name,
                'varasto': Varasto(capacity, initial_stock)
            }
            flash(f'Warehouse "{name}" created successfully!', 'success')
            return redirect(url_for('index'))
        except ValueError:
            flash('Invalid number format', 'error')
            return redirect(url_for('create_warehouse'))

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def warehouse_detail(warehouse_id):
    """View warehouse details."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))

    warehouse = warehouses[warehouse_id]
    return render_template('detail.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    """Add items to warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
        if amount > 0:
            warehouses[warehouse_id]['varasto'].lisaa_varastoon(amount)
            flash(f'Added {amount} units to warehouse', 'success')
        else:
            flash('Amount must be greater than 0', 'error')
    except ValueError:
        flash('Invalid number format', 'error')

    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    """Remove items from warehouse."""
    if warehouse_id not in warehouses:
        flash('Warehouse not found', 'error')
        return redirect(url_for('index'))

    try:
        amount = float(request.form.get('amount', 0))
        if amount > 0:
            removed = warehouses[warehouse_id]['varasto'].ota_varastosta(amount)
            flash(f'Removed {removed} units from warehouse', 'success')
        else:
            flash('Amount must be greater than 0', 'error')
    except ValueError:
        flash('Invalid number format', 'error')

    return redirect(url_for('warehouse_detail', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    """Delete a warehouse."""
    if warehouse_id in warehouses:
        name = warehouses[warehouse_id]['name']
        del warehouses[warehouse_id]
        flash(f'Warehouse "{name}" deleted successfully!', 'success')
    else:
        flash('Warehouse not found', 'error')

    return redirect(url_for('index'))


if __name__ == '__main__':
    # DEVELOPMENT ONLY: Debug mode should be False in production
    app.run(debug=True)
