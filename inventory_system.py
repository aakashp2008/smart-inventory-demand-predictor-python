import os
import json
import csv
from datetime import datetime

class InventorySystem:
    def __init__(self):
        self.products = []
        self.sales_history = []
        self.suppliers = []
        
    def display_menu(self):
        """Displays the main application menu."""
        print("\n" + "="*50)
        print("     SMART INVENTORY & DEMAND PREDICTOR SYSTEM")
        print("="*50)
        print("1. Product Management")
        print("2. Sales & Inventory Operations")
        print("3. Demand Prediction & Restock Recommendations")
        print("4. Supplier Management")
        print("5. Analytics Dashboard & Reports")
        print("6. Data Storage (Load/Save CSV & JSON)")
        print("7. Exit")
        print("="*50)

    # ==========================================
    # MODULE 1: PRODUCT MANAGEMENT
    # ==========================================
    def product_management_menu(self):
        while True:
            print("\n--- Product Management ---")
            print("1. Add New Product")
            print("2. View All Products")
            print("3. Search Product")
            print("4. Update Product")
            print("5. Delete Product")
            print("6. Back to Main Menu")
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '3':
                self.search_product()
            elif choice == '4':
                self.update_product()
            elif choice == '5':
                self.delete_product()
            elif choice == '6':
                break
            else:
                print("❌ Invalid option. Please choose between 1 and 6.")

    def add_product(self):
        print("\n--- Add New Product ---")
        product_id = input("Enter Product ID (e.g., P001): ").strip()
        
        if any(p['product_id'] == product_id for p in self.products):
            print("❌ Error: Product ID already exists.")
            return

        name = input("Enter Product Name: ").strip()
        category = input("Enter Category: ").strip()
        
        try:
            stock = int(input("Enter Current Stock Quantity: "))
            price = float(input("Enter Unit Price ($): "))
            min_threshold = int(input("Enter Low-Stock Alert Threshold: "))
        except ValueError:
            print("❌ Invalid numeric input.")
            return

        new_product = {
            "product_id": product_id,
            "name": name,
            "category": category,
            "stock": stock,
            "price": price,
            "min_threshold": min_threshold
        }
        
        self.products.append(new_product)
        print(f"✅ Success: Product '{name}' added successfully!")

    def view_products(self):
        print("\n--- Current Inventory Products ---")
        if not self.products:
            print("📂 No products found in inventory.")
            return

        print(f"{'ID':<10} | {'Name':<20} | {'Category':<15} | {'Stock':<8} | {'Price ($)':<10} | {'Threshold':<10}")
        print("-" * 80)
        for p in self.products:
            print(f"{p['product_id']:<10} | {p['name']:<20} | {p['category']:<15} | {p['stock']:<8} | {p['price']:<10.2f} | {p['min_threshold']:<10}")

    def search_product(self):
        query = input("Enter Product ID or Name to search: ").strip().lower()
        results = [p for p in self.products if query in p['product_id'].lower() or query in p['name'].lower()]
        
        if not results:
            print("❌ No matching products found.")
            return

        print(f"\n--- Search Results ({len(results)}) ---")
        print(f"{'ID':<10} | {'Name':<20} | {'Category':<15} | {'Stock':<8} | {'Price ($)':<10}")
        print("-" * 70)
        for p in results:
            print(f"{p['product_id']:<10} | {p['name']:<20} | {p['category']:<15} | {p['stock']:<8} | {p['price']:<10.2f}")

    def update_product(self):
        product_id = input("Enter Product ID to update: ").strip()
        product = next((p for p in self.products if p['product_id'] == product_id), None)
        
        if not product:
            print("❌ Product not found.")
            return

        print(f"Updating Product: {product['name']} (Leave blank to keep current value)")
        name = input(f"New Name [{product['name']}]: ").strip()
        category = input(f"New Category [{product['category']}]: ").strip()
        stock_str = input(f"New Stock [{product['stock']}]: ").strip()
        price_str = input(f"New Price [{product['price']}]: ").strip()
        threshold_str = input(f"New Threshold [{product['min_threshold']}]: ").strip()

        if name: product['name'] = name
        if category: product['category'] = category
        if stock_str: product['stock'] = int(stock_str)
        if price_str: product['price'] = float(price_str)
        if threshold_str: product['min_threshold'] = int(threshold_str)

        print("✅ Product updated successfully!")

    def delete_product(self):
        product_id = input("Enter Product ID to delete: ").strip()
        product = next((p for p in self.products if p['product_id'] == product_id), None)
        
        if not product:
            print("❌ Product not found.")
            return

        confirm = input(f"Are you sure you want to delete '{product['name']}'? (y/n): ").strip().lower()
        if confirm == 'y':
            self.products.remove(product)
            print("🗑️ Product deleted successfully.")
        else:
            print("Operation cancelled.")

    # ==========================================
    # MODULE 2: SALES & INVENTORY OPERATIONS
    # ==========================================
    def sales_operations_menu(self):
        while True:
            print("\n--- Sales & Inventory Operations ---")
            print("1. Record New Sale")
            print("2. View Sales History")
            print("3. Check Low-Stock Alerts")
            print("4. Back to Main Menu")
            
            choice = input("Select an option (1-4): ").strip()
            
            if choice == '1':
                self.record_sale()
            elif choice == '2':
                self.view_sales_history()
            elif choice == '3':
                self.check_low_stock()
            elif choice == '4':
                break
            else:
                print("❌ Invalid option.")

    def record_sale(self):
        print("\n--- Record Sale ---")
        product_id = input("Enter Product ID sold: ").strip()
        product = next((p for p in self.products if p['product_id'] == product_id), None)
        
        if not product:
            print("❌ Product not found.")
            return

        try:
            qty = int(input(f"Enter Quantity Sold (Available: {product['stock']}): "))
        except ValueError:
            print("❌ Invalid quantity.")
            return

        if qty <= 0:
            print("❌ Quantity must be greater than zero.")
            return

        if qty > product['stock']:
            print("❌ Error: Insufficient stock available.")
            return

        product['stock'] -= qty
        sale_record = {
            "product_id": product_id,
            "product_name": product['name'],
            "quantity": qty,
            "total_price": qty * product['price'],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.sales_history.append(sale_record)
        print(f"✅ Sale recorded successfully! Total: ${sale_record['total_price']:.2f}")

    def view_sales_history(self):
        print("\n--- Sales History ---")
        if not self.sales_history:
            print("📂 No sales recorded yet.")
            return

        print(f"{'Date':<20} | {'ID':<8} | {'Product Name':<18} | {'Qty':<5} | {'Total ($)':<10}")
        print("-" * 75)
        for s in self.sales_history:
            print(f"{s['date']:<20} | {s['product_id']:<8} | {s['product_name']:<18} | {s['quantity']:<5} | {s['total_price']:<10.2f}")

    def check_low_stock(self):
        print("\n--- Low-Stock Alerts ---")
        low_stock_items = [p for p in self.products if p['stock'] <= p['min_threshold']]
        
        if not low_stock_items:
            print("✅ All stock levels are healthy.")
            return

        print(f"{'ID':<10} | {'Name':<20} | {'Stock':<8} | {'Threshold':<10}")
        print("-" * 55)
        for p in low_stock_items:
            print(f"⚠️ {p['product_id']:<8} | {p['name']:<20} | {p['stock']:<8} | {p['min_threshold']:<10}")

    # ==========================================
    # MODULE 3: DEMAND PREDICTION & RESTOCK
    # ==========================================
    def demand_prediction_menu(self):
        while True:
            print("\n--- Demand Prediction & Restock Recommendations ---")
            print("1. Predict Future Demand & Restock Recommendations")
            print("2. Back to Main Menu")
            
            choice = input("Select an option (1-2): ").strip()
            if choice == '1':
                self.predict_demand()
            elif choice == '2':
                break
            else:
                print("❌ Invalid option.")

    def predict_demand(self):
        print("\n--- Demand Prediction Report (7-Day Forecast) ---")
        if not self.products:
            print("📂 No products available.")
            return

        print(f"{'ID':<8} | {'Product Name':<18} | {'Current Stock':<13} | {'Est. 7D Demand':<15} | {'Recommended Restock':<18}")
        print("-" * 80)
        for p in self.products:
            # Calculate demand based on historical sales or fallback baseline
            product_sales = sum(s['quantity'] for s in self.sales_history if s['product_id'] == p['product_id'])
            # Simple algorithmic projection: daily average scale or heuristic demand
            estimated_7d_demand = max(5, product_sales + 3)
            
            restock_needed = max(0, estimated_7d_demand - p['stock'])
            print(f"{p['product_id']:<8} | {p['name']:<18} | {p['stock']:<13} | {estimated_7d_demand:<15} | {restock_needed:<18}")

    # ==========================================
    # MODULE 4: SUPPLIER MANAGEMENT
    # ==========================================
    def supplier_management_menu(self):
        while True:
            print("\n--- Supplier Management ---")
            print("1. Add Supplier")
            print("2. View Suppliers")
            print("3. Back to Main Menu")
            
            choice = input("Select an option (1-3): ").strip()
            if choice == '1':
                self.add_supplier()
            elif choice == '2':
                self.view_suppliers()
            elif choice == '3':
                break
            else:
                print("❌ Invalid option.")

    def add_supplier(self):
        print("\n--- Add Supplier ---")
        supp_id = input("Enter Supplier ID: ").strip()
        name = input("Enter Supplier Name: ").strip()
        contact = input("Enter Contact Email/Phone: ").strip()
        item = input("Enter Supplied Product Category/Name: ").strip()

        supplier = {
            "supplier_id": supp_id,
            "name": name,
            "contact": contact,
            "item": item
        }
        self.suppliers.append(supplier)
        print("✅ Supplier added successfully!")

    def view_suppliers(self):
        print("\n--- Registered Suppliers ---")
        if not self.suppliers:
            print("📂 No suppliers recorded.")
            return

        print(f"{'ID':<10} | {'Name':<20} | {'Contact':<20} | {'Supplied Item':<15}")
        print("-" * 70)
        for s in self.suppliers:
            print(f"{s['supplier_id']:<10} | {s['name']:<20} | {s['contact']:<20} | {s['item']:<15}")

    # ==========================================
    # MODULE 5: ANALYTICS DASHBOARD & REPORTS
    # ==========================================
    def analytics_menu(self):
        while True:
            print("\n--- Analytics Dashboard & Reports ---")
            print("1. View Inventory Summary & Revenue")
            print("2. Back to Main Menu")
            
            choice = input("Select an option (1-2): ").strip()
            if choice == '1':
                self.show_analytics()
            elif choice == '2':
                break
            else:
                print("❌ Invalid option.")

    def show_analytics(self):
        print("\n" + "="*40)
        print("         ANALYTICS DASHBOARD")
        print("="*40)
        total_products = len(self.products)
        total_stock_units = sum(p['stock'] for p in self.products)
        total_inventory_value = sum(p['stock'] * p['price'] for p in self.products)
        total_revenue = sum(s['total_price'] for s in self.sales_history)

        print(f"📦 Total Unique Products : {total_products}")
        print(f"📊 Total Stock Items     : {total_stock_units}")
        print(f"💰 Total Inventory Value : ${total_inventory_value:.2f}")
        print(f"📈 Total Sales Revenue   : ${total_revenue:.2f}")
        print("="*40)

    # ==========================================
    # MODULE 6: DATA STORAGE (JSON & CSV)
    # ==========================================
    def storage_menu(self):
        while True:
            print("\n--- Data Storage ---")
            print("1. Save Data (JSON)")
            print("2. Load Data (JSON)")
            print("3. Export Products to CSV")
            print("4. Back to Main Menu")
            
            choice = input("Select an option (1-4): ").strip()
            if choice == '1':
                self.save_json()
            elif choice == '2':
                self.load_json()
            elif choice == '3':
                self.export_csv()
            elif choice == '4':
                break
            else:
                print("❌ Invalid option.")

    def save_json(self, filename="inventory_data.json"):
        data = {
            "products": self.products,
            "sales_history": self.sales_history,
            "suppliers": self.suppliers
        }
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"✅ Data successfully saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving file: {e}")

    def load_json(self, filename="inventory_data.json"):
        if not os.path.exists(filename):
            print(f"❌ File {filename} not found.")
            return
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.products = data.get("products", [])
                self.sales_history = data.get("sales_history", [])
                self.suppliers = data.get("suppliers", [])
            print(f"✅ Data successfully loaded from {filename}")
        except Exception as e:
            print(f"❌ Error loading file: {e}")

    def export_csv(self, filename="products_export.csv"):
        if not self.products:
            print("📂 No product data to export.")
            return
        try:
            keys = self.products[0].keys()
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(self.products)
            print(f"✅ Products successfully exported to {filename}")
        except Exception as e:
            print(f"❌ Error exporting CSV: {e}")

# ==========================================
# APPLICATION ENTRY POINT
# ==========================================
if __name__ == "__main__":
    app = InventorySystem()
    while True:
        app.display_menu()
        main_choice = input("Select an option (1-7): ").strip()
        
        if main_choice == '1':
            app.product_management_menu()
        elif main_choice == '2':
            app.sales_operations_menu()
        elif main_choice == '3':
            app.demand_prediction_menu()
        elif main_choice == '4':
            app.supplier_management_menu()
        elif main_choice == '5':
            app.analytics_menu()
        elif main_choice == '6':
            app.storage_menu()
        elif main_choice == '7':
            print("Exiting application. Goodbye!")
            break
        else:
            print("❌ Invalid option. Please choose between 1 and 7.")
