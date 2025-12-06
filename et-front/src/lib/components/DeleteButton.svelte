<script>
    import { createEventDispatcher } from "svelte";

    export let id = null;

    const dispatch = createEventDispatcher();

    function handleClick() {
        dispatch('handleDelete', {
            id: id
        })
    }
</script>

<button on:click={handleClick} title="Удалить" style="all: unset; cursor: pointer;"><i class="bi bi-trash3 text-danger"></i></button>