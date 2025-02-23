// Fetch data from GraphQL API
async function fetchDashboardData() {
  const response = await fetch('http://localhost:8000/graphql', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: `
  query {
    allProperties {
      id
    }
    allMovements {
      id
      property {
        name
      }
      originDepartment {
        name
      }
      destinationDepartment {
        name
      }
      timestamp
    }
    all_maintenance {  // Corrigido para minúsculas
      id
      scheduled_date
      completion_date
    }
  }
      `,
    }),
  });

  const data = await response.json();
  return data.data;
}

// Update DOM with data
async function renderDashboard() {
  const data = await fetchDashboardData();
  document.getElementById('total-assets').textContent = data.allProperties.length;

  // Render recent movements
  const movementsContainer = document.getElementById('recent-movements');
  movementsContainer.innerHTML = '';
  data.allMovements.slice(0, 5).forEach(movement => {
    const movementElement = document.createElement('div');
    movementElement.className = 'mb-2';
    movementElement.textContent = `${movement.property.name} moveu de ${movement.originDepartment.name} para ${movement.destinationDepartment.name}`;
    movementsContainer.appendChild(movementElement);
  });

  // Calculate pending maintenances
    const pendingMaintenances = data.all_maintenance.filter(m => !m.completion_date);
    document.getElementById('pending-maintenance').textContent = pendingMaintenances.length;
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', renderDashboard);