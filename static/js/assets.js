    async function fetchProperties() {
      const response = await fetch('/api/properties/');
      const data = await response.json();
      // Atualizar tabela com dados
    }