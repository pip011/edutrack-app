<script>
    import ProtectedPage from "$lib/components/ProtectedPage.svelte";
</script>

<ProtectedPage requiredRole='student'>
    <h1>Привет, студент</h1>
</ProtectedPage>