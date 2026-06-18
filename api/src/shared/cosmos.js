const { CosmosClient } = require('@azure/cosmos');

// Single cached container handle. Connection + names come from SWA app settings.
let container;

function getContainer() {
  if (container) return container;
  const connectionString = process.env.COSMOS_CONNECTION_STRING;
  if (!connectionString) throw new Error('COSMOS_CONNECTION_STRING is not set');
  const dbName = process.env.COSMOS_DB || 'training';
  const containerName = process.env.COSMOS_CONTAINER || 'progress';
  const client = new CosmosClient(connectionString);
  container = client.database(dbName).container(containerName);
  return container;
}

module.exports = { getContainer };
