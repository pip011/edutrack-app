<script>
    import EditableRow from '$lib/components/EditableRow.svelte';
    import { PUBLIC_API_URL } from '$env/static/public';
    import { error } from '@sveltejs/kit';
    import { fly, fade } from 'svelte/transition';
    import { invalidate } from '$app/navigation';

    export let data = null;
    let selectedGroupId = "";
    let selectedStudentId = null;
    let isLoading = false;
    let isSuccess = true; 
    let successMessage = '';
    let errorMessage = '';
    let notification = false;
    let studentIdToAdd = null;
    let showAddStudentForm = false;
    let showCreateGroupForm = false;
    let groupYearToAdd = null;
    let groupNameToAdd = null;

    function showNotification() {
      notification = true;
      setTimeout(() => {
        notification = false;
      }, 3000)
    }

    $: selectedGroup = data
		    ? data.groups.find(g => String(g.id) === String(selectedGroupId))
		    : null;
      
    $: if (selectedGroupId != null) {
        selectedStudentId = null;
        showAddStudentForm = false;
    }

    function deleteGroupById(idToDelete) {
		  data.groups = data.groups.filter(group => group.id !== idToDelete);
	  }

    async function handleDeleteStudent() {
      let body = {};
      body['student_id'] = selectedStudentId;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups/unbind-student`, {
            credentials: 'include', 
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            let jsonData = await response.json();
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + jsonData.detail;
            showNotification()
            return
        }

        await invalidate('app:groups');
        selectedStudentId = null;

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    function addStudentToDataGroup(group_id, student) {
        showAddStudentForm = false;

        const oldGroup = data.groups.find(g =>
            g.students.some(s => s.id === student.id)
        );
    
        if (oldGroup) {
            oldGroup.students = oldGroup.students.filter(s => s.id !== student.id);
        }
      
        const newGroup = data.groups.find(g => g.id === group_id);
        if (!newGroup) return;
      
        newGroup.students = [...newGroup.students, student];
      
        data = { ...data };
    }

    function handleRClick(event) {
      selectedStudentId = event.detail.rowId;
    }

    async function handleDeleteGroup() {
      isLoading = true;
      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups/delete/${selectedGroupId}`, {
            credentials: 'include', 
            method: 'POST'
        });

        if (!response.ok) {
            isLoading = false;
            isSuccess = false;
            errorMessage = 'Операция выполнена безуспешно.'
            showNotification()
            return
        }
        
        deleteGroupById(selectedGroupId);
        selectedGroupId = '';
        selectedStudentId = null;
        isLoading = false;
        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isLoading = false;
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.error
      } finally {
        showNotification()
      }
    }

    function handleCancelChoose() {
      selectedStudentId = null;
    }

    function handleCreateGroupForm() {
      showCreateGroupForm ? showCreateGroupForm = false : showCreateGroupForm = true;
      groupNameToAdd = '';
      groupYearToAdd = '';
    }

    async function handleAddGroup() {
      let body = {};
      body['name'] = groupNameToAdd;
      body['year_start'] = groupYearToAdd;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups`, {
            credentials: 'include', 
            method: 'POST', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            errorMessage = 'Операция выполнена безуспешно. Ошибка: ' + response.statusText
            showNotification()
            return
        }

        let group = await response.json()
        group.students = []
        data.groups.push(group)
        data = { ...data }

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    async function handleAddStudent() {
      if (studentIdToAdd === null || studentIdToAdd === '') {
        return;
      }

      const group = data.groups.find(g => g.id === selectedGroupId);
      const student = group.students.find(s => s.id === studentIdToAdd)
      if (student) {
        isSuccess = false;
        errorMessage = 'Операция выполнена безуспешно. Данный студент уже есть в группе.'
        showNotification()
        return
      }

      let body = {};
      body['student_id'] = studentIdToAdd;
      body['group_id'] = selectedGroupId;

      try {
        const response = await fetch(`${PUBLIC_API_URL}/api/groups/add-student`, {
            credentials: 'include', 
            method: 'PATCH', 
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            isSuccess = false;
            if (response.status === 404) {
              errorMessage = 'Операция выполнена безуспешно. Такого студента не существует.'
            } else {
              errorMessage = 'Операция выполнена безуспешно.'
            }
            showNotification()
            return
        }

        let student = await response.json()
        addStudentToDataGroup(selectedGroupId, student)

        isSuccess = true;
        successMessage = 'Операция выполнена успешно.'

      } catch (e) {
        isSuccess = false;
        errorMessage = 'Ошибка: ' + e.message
      } finally {
        showNotification()
      }
    }

    function handleAddStudentForm() {
      showAddStudentForm ? showAddStudentForm = false : showAddStudentForm = true;
      studentIdToAdd = '';
    }
</script>

<div class="d-flex flex-column" style="max-width: 65%">
    <h2 class="mb-4 text-white">Группы</h2>
    {#if !data}
    <div class='d-flex justify-content-center'>
        <div class="spinner-border text-primary" style="width: 3rem; height: 3rem;"></div>
    </div>
    {:else if data.error}
    <p class="text-danger">{data.error}</p>
    {:else}
<div class="form-floating mb-4">
  <select
    class="form-select bg-dark text-white border-secondary w-50"
    id="floatingSelect"
    aria-label="Floating label select example"
    bind:value={selectedGroupId}>
    <option value="">Группа не выбрана</option>
    {#each data.groups as group}
      <option value={group.id}>{group.name}</option>
    {/each}
  </select>
  <label class="text-secondary" for="floatingSelect">Группа</label>
</div>
    {/if}
    {#if selectedGroupId != ""}
    <h3 class="mb-4 text-white mb-2">Список студентов</h3>
    <table class="table table-dark table-hover w-50">
      <thead class="table-dark">
        <tr>
          <th>№</th>
          <th>Имя студента</th>
        </tr>
      </thead>
      <tbody>
        {#each selectedGroup.students as student, i}
			  	<EditableRow on:handleRowClick={handleRClick} rowId={student.id} items={[i+1, student.full_name]} />
		    {/each}
      </tbody>
    </table>
    {#if isLoading}
    <span class="spinner-border spinner-border-sm" style="position: absolute; right: 0; top: 0;"></span>
    {:else}
      {#if selectedStudentId}
      <div class="d-flex gap-2">
        <button on:click={handleDeleteStudent} class="btn btn-danger">Удалить</button>
        <button on:click={handleCancelChoose} class="btn btn-secondary">Отменить выбор</button>
      </div>
      {:else}
      <div class="f-flex gap-2">
        {#if showAddStudentForm}
        <div class="d-flex flex-column gap-1">
          <h6 class="text-white">Введите ID студента</h6>
          <div class="input-group mb-3 w-25">
            <button on:click={handleAddStudent} class="btn btn-outline-primary" type="button" id="button-addon1">Добавить</button>
            <input bind:value={studentIdToAdd} type="number" class="form-control bg-dark text-white border-secondary" placeholder="Введите ID студента" aria-label="Example text with button addon" aria-describedby="button-addon1">
          </div>
          <button on:click={handleAddStudentForm} class="btn btn-secondary" style="width: 8rem;">Вернуться</button>
        </div>
        {:else}
          <button on:click={handleAddStudentForm} class="btn btn-primary">Добавить студента</button>
        {/if}
      </div>
      {/if}
    {/if}

    <div class="d-flex flex-column gap-2 mt-4">
      <h3 class="text-white">Действия с группой</h3>
      <div class="d-flex gap-2">
        <button on:click={handleDeleteGroup} class="btn btn-danger">Удалить группу</button>
      </div>
    </div>

    {/if}

    {#if selectedGroupId === ''}
    <div class="d-flex flex-column gap-2">
      <h4 class="text-white">Действия</h4>
      {#if showCreateGroupForm}
      <div class="d-flex flex-column p-1">
          <h5 class="mb-3 text-white">Создать группу</h5>
          <h6 class="mb-1 text-white">Название группы</h6>
          <div class="input-group mb-2 w-25">
            <input bind:value={groupNameToAdd} type="text" class="form-control bg-dark text-white border-secondary mb-2 w-50" placeholder="Введите название группы">
          </div>
          <h6 class="mb-1 text-white">Год начала</h6>
          <div class="input-group mb-4 w-25">
            <input bind:value={groupYearToAdd} type="number" class="form-control bg-dark text-white border-secondary" placeholder="Введите название группы">
          </div>
          <div class="d-flex flex-row gap-2">
            <button on:click={handleAddGroup} class="btn btn-primary align-self-start">Создать</button>
            <button on:click={handleCreateGroupForm} class="btn btn-secondary align-self-start">Вернуться</button>
          </div>
      </div>
      {:else}
      <button on:click={handleCreateGroupForm} class="btn btn-success align-self-start">Создать группу</button>
      {/if}
    </div>
    {/if}

    {#if notification}
    <div 
      class={isSuccess ? "alert alert-success" : "alert alert-danger"}
      role="alert"
      style="
        width: auto;
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1050;
        min-width: 200px;
      "
      in:fly={{ x: 100, duration: 300 }}
      out:fly={{ x: 100, duration: 300 }}
    >
      {isSuccess ? successMessage : errorMessage}
    </div>
    {/if}
</div>