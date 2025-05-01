from google.cloud import spanner_v1


async def upsert_spanner_async(project: str, instance : str, database : str, table : str, columns : list, values : list):
    # Create a client
    client = spanner_v1.SpannerAsyncClient()

    database_path = f"projects/{project}/instances/{instance}/databases/{database}"

        # Initialize request argument(s)
    session_request = spanner_v1.BatchCreateSessionsRequest(
        database=database_path,
        session_count=1,
    )

    # Make the request
    session_response = await client.batch_create_sessions(request=session_request)

    # Handle the response
    print(session_response)

    # Initialize request argument(s)
    with  spanner_v1.MutationGroup() as mutation_groups:
        mutation_group = mutation_groups.group()
        mutation_group.insert_or_update(
            table=table,
            columns=columns,
            values=values,
        )

        request = spanner_v1.BatchWriteRequest(
            session=session_response,
            mutation_groups=mutation_groups,
        )

        # Make the request
        stream = await client.batch_write(request=request)

        # Handle the response
        async for response in stream:
            print(response)