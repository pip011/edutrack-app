<script>
    import { createEventDispatcher } from 'svelte';
    import { PUBLIC_API_URL } from '$env/static/public';

    export let value;
    export let field;
    export let entity;
    export let userId;
    export let isBirthDate = false;

    let editingValue = value;
    let isLoading = false;
    let error = null;
    let timeout;

    $: editingValue = (() => {
    if (field === 'birth_date' && value) {
      try {
        return new Date(value).toISOString().split('T')[0];
      } catch {
        return '';
      }
    }
    return value ?? '';
  })();

    const dispatch = createEventDispatcher();

    async function save() {
      isLoading = true;
      error = null;

      let body = {}
      body[entity] = { [field]: editingValue }

      try {
        const res = await fetch(`${PUBLIC_API_URL}/api/users/${userId}`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(body)
        });

        if (!res.ok) throw new Error(`Ошибка ${res.status}`);

        const updated = await res.json();
        dispatch('update', updated.user);
      } catch (e) {
        console.error(e);
        error = e.message;
        editingValue = value;
      } finally {
        isLoading = false;
      }
    }

    function handleBlur() {
      if (editingValue !== value) save();
    }

    function handleInput() {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        save();
      }, 1500)
    }
</script>

<div style="position: relative;">
  {#if isBirthDate}
  <input 
    type="date" 
    bind:value={editingValue} 
    on:change={handleInput}
    style="all: unset; cursor: pointer;"
  />
  {:else}
  <input
    type="text" 
    bind:value={editingValue} 
    on:input={handleInput}
    style="all: unset; cursor: pointer; accent-color: white;"
  />
  {/if}

  {#if isLoading}
    <span class="spinner-border spinner-border-sm" style="position: absolute; right: 0; top: 0;"></span>
  {/if}
</div>

{#if error}
  <div class="text-danger small">{error}</div>
{/if}