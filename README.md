# Order-and-Warehouse-Management-Application
Inventory and Order Management Project

This project is an application developed with Streamlit that manages an inventory system, order registration, data modification, and visualization of relevant information for a company that handles products, clients, and materials.

Main Features

1. Order Registration

Allows registration of client orders.

Selection of products, quantities, and additional details such as priority, payment type, delivery date, and time.

Data validation to avoid registration errors.

2. Inventory

Entry and Exit Records:

Manages materials entering or leaving the inventory.

Calculates unit prices based on currency conversion (Bolívares, Pesos, or Dollars).

Verifies available quantities before making exits.

3. Data Visualization

Enables consulting existing orders:

Orders scheduled for the current day.

Pending orders for the week.

Consolidates information about orders, products, and clients.

4. Data Modification

Modifies existing data of clients, products, orders, and materials.

Updates data in real-time and allows direct editing.

5. New Data Registration

Allows adding new clients, products, and materials with validations to avoid duplicates.

Project Structure

The project is divided into independent modules to facilitate organization and scalability.

Main Files:

main.py: Main entry point of the application.

Configures the main tabs of the application: Order registration, inventory, new data registration, visualization, and modification.

registro_tab.py: Handles the logic for registering new orders.

almacen_tab.py: Manages inventory with entry and exit records.

nuevo_tab.py: Allows registration of new clients, products, and materials.

visualizacion_tab.py: Displays scheduled and pending orders, with filtering and grouping options.

modificacion_tab.py: Allows modification of existing data for clients, products, and orders.

datos.py: Provides functions to:

Create initial CSV files if they don't exist.

Register clients, products, and orders in the corresponding files.

Validate and update data in existing CSV files.

System Requirements

Python 3.10 or higher.

Additional dependencies specified in requirements.txt:

pandas
streamlit

Instructions to Run

Clone the repository:

git clone <REPOSITORY_URL>
cd <PROJECT_NAME>

Install the dependencies:

pip install -r requirements.txt

Run the application with Streamlit:

streamlit run main.py

Access the application from your browser at:

http://localhost:8501

Application Usage

Available Tabs:

Order Registration:

Select an existing client or register a new one.

Add products and quantities.

Define priority, payment type, and delivery date.

Inventory:

Register entries and exits of materials.

Manage unit prices with currency conversion.

Check existing materials and available balance.

New Data:

Register new clients, products, or materials.

Visualization:

Consult daily and weekly orders.

Verify details of related products and clients.

Modification:

Edit client, product, and order information directly from the interface.

Additional Considerations

Data is stored in CSV format within the datos folder.

Ensure initial CSV files are created before running the system.

The project can be expanded to use a relational database if greater scalability is required.

Contribution

If you wish to contribute:

Fork the repository.

Create a branch for your feature or fix:

git checkout -b new_feature

Submit a pull request with your changes.

License

This project is licensed under the MIT License. You can use and modify it freely for personal or commercial purposes.

