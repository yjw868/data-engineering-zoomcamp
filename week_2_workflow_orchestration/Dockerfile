FROM prefecthq/prefect:2.7.7-python3.9 as base

COPY requirements.txt .

RUN pip install --upgrade pip & \
    pip install psycopg2-binary & \
    pip install -r requirements.txt --trusted-host pypi.python.org --no-cache-dir

COPY flows /opt/prefect/flows
RUN mkdir -p /opt/prefect/data/yellow

# # ----------------------------------------- #
# #                  Runner
# # ----------------------------------------- #
FROM base AS runner
# EXPOSE 4200 
# CMD ["python", "orion", "start"]

# # ----------------------------------------- #
# #                  Agent
# # ----------------------------------------- #
# FROM orion AS agent
# CMD ["prefect", "agent", "start"]