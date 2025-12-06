<script>
    import { createEventDispatcher } from "svelte";

    export let rowId = null;
    export let items = []

    const dispatch = createEventDispatcher()

    function handleClick() {
        dispatch('handleRowClick', {
            rowId: rowId
        })
    }
</script>

<tr style="cursor: pointer;"
    on:click={handleClick}
>
    {#each items as item}
      <td>
        {#if typeof item === 'function'} 
          <svelte:component this={item} /> 
        {:else}
        {item}
        {/if}
      </td>
    {/each}
</tr>