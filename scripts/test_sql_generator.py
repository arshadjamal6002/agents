from agents.sql_generator_agent.prompt import build_sql_prompt

# print(build_sql_prompt(
#     instruction="Get the top 10 products by quantity sold",
#     table_schema="orders(product_id, quantity, date)",
#     dialect="PostgreSQL"
# ))

# ##############################################

# sample = {
#     "instruction": "List all employees hired after 2020",
#     "table_schema": "employees(id, name, hire_date)",
#     "dialect": "MySQL"
# }

# from agents.sql_generator_agent.tool import tool
# print(tool(sample))

#################################################

from agents.sql_generator_agent.tool import tool

print(tool({
    "instruction": "Show average salary by department",
    "table_schema": "employees(id, name, department, salary)",
    "dialect": "PostgreSQL"
}))


###################################################

