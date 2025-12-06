<script>
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { checkAuth } from '$lib/utils/auth.js';

  onMount(async () => {
      goto('/login');
  })
</script>