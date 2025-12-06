<script>
  import ProtectedPage from "$lib/components/ProtectedPage.svelte";
  import LogoutButton from "$lib/components/LogoutButton.svelte";
</script>
<ProtectedPage requiredRole='teacher'>
  <div class="container-fluid" style="background-color: #292938;">
    <div class="f-flex row" style="height: auto; min-height: 100vh; width: auto; min-width: 100vh;">
      
      <div class="col-auto bg-dark text-white p-3 d-flex flex-column" style="flex: 0 0 11%;">
          <nav class="navbar">
            <div class="container-fluid">
              <ul class="nav flex-column">
                <li class="nav-item">
                  <a class="nav-link text-white" href="/t/gradebook">Журнал оценок</a>
                </li>
              </ul>
            </div>
          </nav>
          <LogoutButton/>
      </div>
    
      <div class="col-auto p-4" style="flex: 1">
          <slot />
      </div>
    
    </div>
  </div>
</ProtectedPage>