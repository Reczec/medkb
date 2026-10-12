targetScope = 'resourceGroup'

param appName string
param environmentName string = '${appName}-env'
@allowed(['westeurope', 'northeurope'])
param location string = 'northeurope'
param image string
@secure()
param appSecrets object
param secretEnv array
param ragEnabled bool = false

resource environment 'Microsoft.App/managedEnvironments@2025-07-01' = {
  name: environmentName
  location: location
  tags: { project: 'medkb-azure-demo' }
  properties: {
    appLogsConfiguration: {}
    workloadProfiles: [
      { name: 'Consumption', workloadProfileType: 'Consumption' }
    ]
    zoneRedundant: false
  }
}

resource app 'Microsoft.App/containerApps@2025-07-01' = {
  name: appName
  location: location
  tags: { project: 'medkb-azure-demo' }
  properties: {
    environmentId: environment.id
    workloadProfileName: 'Consumption'
    configuration: {
      activeRevisionsMode: 'Single'
      secrets: appSecrets.items
      ingress: {
        external: true
        allowInsecure: false
        targetPort: 8000
        transport: 'auto'
      }
    }
    template: {
      containers: [
        {
          name: 'medkb'
          image: image
          resources: { cpu: json('0.5'), memory: '1Gi' }
          env: concat([
            { name: 'PORT', value: '8000' }
            { name: 'DEMO_MODE', value: 'true' }
            { name: 'DEMO_RESET_HOURS', value: '3' }
            { name: 'CLIENT_IP_HEADER', value: 'X-Forwarded-For' }
            { name: 'AI_BASE_URL', value: 'https://generativelanguage.googleapis.com/v1beta/openai' }
            { name: 'AI_MODEL', value: 'gemini-3.5-flash-lite' }
            { name: 'AI_DAILY_LIMIT', value: '500' }
            { name: 'AI_CLIENT_DAILY_LIMIT', value: '30' }
            { name: 'RAG_ENABLED', value: string(ragEnabled) }
            { name: 'RAG_MIN_SIMILARITY', value: '0.60' }
          ], secretEnv)
          probes: [
            {
              type: 'Startup'
              httpGet: { path: '/api/health', port: 8000, scheme: 'HTTP' }
              periodSeconds: 5
              failureThreshold: 60
            }
            {
              type: 'Readiness'
              httpGet: { path: '/api/health', port: 8000, scheme: 'HTTP' }
              periodSeconds: 10
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 1
        rules: [
          { name: 'http', http: { metadata: { concurrentRequests: '10' } } }
        ]
      }
    }
  }
}

output hostname string = app.properties.configuration.ingress.fqdn
