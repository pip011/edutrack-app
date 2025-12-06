<script>
    import { onMount } from 'svelte';
    import ErrorPage from '$lib/components/ErrorPage.svelte';
    import { checkAuth } from '$lib/utils/auth.js';
    import { goto } from '$app/navigation'

    export let requiredRole = null;
    let showError = false;
    let contentReady = false;

    onMount(async () => {
        let userRole = null;
        let userData = null;

        try {
            userData = await checkAuth();

            if (userData) {
                userRole = userData.role;
            } else {
                goto('/login')
                return; 
            }

            if (!userData || (requiredRole && userRole !== requiredRole)) {
                showError = true;
            }
            
            contentReady = true;
        } catch (error) {
            console.error('Mount error:', error);
            showError = true;
            contentReady = true;
        }
    });
</script>

{#if !contentReady}
<div class="d-flex justify-content-center align-items-center" style="height: 100vh ;">
    <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
</div>
{:else if showError}
  <ErrorPage />
{:else}
  <slot />
{/if}