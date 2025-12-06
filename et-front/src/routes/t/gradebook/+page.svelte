<script>
    import { loadGradesBySubjectWithYearAndMonth } from '$lib/utils/teacherGradebook.js';
    import { onMount } from 'svelte';
    import EditableGradeCell from '$lib/components/EditableGradeCell.svelte';
    import { saveGrade } from '$lib/utils/saveGrade.js'
    import { fly, fade } from 'svelte/transition';

    export let data = null;
    
    let grades = null;
    let gradesMap = new Map();
    let selectedSubjectId = ''
    let selectedGroupId = ''
    let monthYear = null;
    let month = null;
    let year = null;
    let timeout;
    let matrixReady = false;
    let matrix = null;

    let notification = false;
    let isSuccess = true;
    let errorMessage = 'Операция прошла безуспешно.'
    let successMessage = 'Операция прошла успешно'
    
    $: gradesMap = grades ? new Map(grades.map(g => [`${g.student_id}-${new Date(g.date).getDate()}`, g])) : new Map();

    $: selectedGroup = data?.groups?.find(g => g.id === selectedGroupId);
    
    $: students = selectedGroup ? selectedGroup.students : [];

    $: bothSelected = selectedSubjectId !== '' && selectedGroupId !== '';

    $: if (monthYear) {
        const [y, m] = monthYear.split("-");
        year = y;
        month = m;
    }

    $: if (month && year && selectedSubjectId !== '' && selectedGroupId !== '') {
        matrixReady = false;
        console.log('Вызов loaxdGrades ============')
        clearTimeout(timeout);
        timeout = setTimeout(() => {  
            loadGradesForSelection()
        }, 500);
    }

    $: days = Array.from({ length: getDaysInMonth(month, year) }, (_, i) => i + 1);

    async function loadGradesForSelection() {
      grades = await loadGradesBySubjectWithYearAndMonth(selectedSubjectId, month, year);
      const safeGrades = Array.isArray(grades) ? grades : [];
      matrix = buildMatrix(students, safeGrades, days, month, year).map(row => ({
        student: row.student,
        days: [...row.days]
      }));
      matrixReady = true;
    }

     onMount(() => {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, "0");

        monthYear = `${y}-${m}`;
    });

    function buildMatrix(students, grades, days, month, year) {
      const gradeMap = new Map();
    
      for (const g of grades) {
        const dateKey = g.date.split("T")[0];
        const key = `${g.student_id}-${dateKey}`;
        gradeMap.set(key, g.grade);
      }
    
      const result = [];
    
      for (const student of students) {
        const row = { student, days: [] };
      
        for (const day of days) {
          const dayStr = String(day).padStart(2, "0");
          const dateKey = `${year}-${String(month).padStart(2, "0")}-${dayStr}`;
          const key = `${student.id}-${dateKey}`;
          row.days.push(gradeMap.get(key) ?? null);
        }
      
        result.push(row);
      }
    
      return result;
    }

    function getDaysInMonth(month, year) {
      return new Date(year, month, 0).getDate();
    }

    async function loadGrades() {
      grades = await loadGradesBySubjectWithYearAndMonth(selectedSubjectId, month, year);
    }

    function showNotification(success, message="Операция прошла успешно") {
      notification = true;
      if (!success) {
        errorMessage = message;
        isSuccess = false;
      } else {
        isSuccess = true;
        successMessage = message;
      }

      setTimeout(
        () => notification = false, 1000
      )
    }

    async function handleSave(cellData) {
      if (!gradesMap) return;
      let res = await saveGrade(cellData, gradesMap);

      if (res.error) {
        let errMessage = res.error
        showNotification(false, errMessage)
      } else {
        showNotification(true)
      }
      
      grades = Array.from(gradesMap.values());
    }

    $: console.log(matrix)
</script>

<div class="d-flex flex-column" style="max-width: 80%">
    <h2 class="mb-4 text-white">Журнал оценок</h2>
    {#if !data}
    <div class='d-flex'>
        <div class="spinner-border text-primary" style="width: 2rem; height: 2rem;"></div>
    </div>
    {:else if data.error}
    <p class="text-danger">{data.error}</p>
    {:else}
    <div class="d-flex flex-row gap-3">
        <div class="form-floating mb-2">
            <select
              class="form-select bg-dark text-white border-secondary w-100"
              id="floatingSelect"
              aria-label="Floating label select example"
              bind:value={selectedSubjectId}>
              <option value="">Предмет не выбран</option>
              {#each data.subjects as subject}
                <option value={subject.id}>{subject.name}</option>
              {/each}
            </select>
            <label class="text-secondary" for="floatingSelect">Предмет</label>
        </div>
        <div class="form-floating mb-2">
            <select
              class="form-select bg-dark text-white border-secondary w-100"
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
    </div>
    {#if bothSelected}
    <label class="text-secondary mb-1" for="inputPeriod">Период</label>
    <input id="inputPeriod" type="month" bind:value={monthYear} class="form-select bg-dark text-white border-secondary mb-3" style="width: 20%;" />
    
    {#if matrixReady}
    <div class="table-responsive">
        <table class="table table-dark table-bordered table-hover">
            <thead class="table-dark">
              <tr>
                <th style=" text-align: left;">ФИО</th>
                {#each days as d}
                  <th style="min-width: 35px; text-align: center;">{d}</th>
                {/each}
              </tr>
            </thead>
            <tbody>
              {#each matrix as row}
              <tr>
                <td style="white-space: nowrap; overflow: hidden; text-overflow: auto;">{row.student.full_name}</td>
              
                {#each row.days as value, index}
                  <EditableGradeCell
                    value={value}
                    studentId={row.student.id}
                    day={days[index]}
                    subjectId={selectedSubjectId}
                    month={month}
                    year={year}
                    onSave={handleSave}
                  />
                {/each}
              </tr>
              {/each}
            </tbody>
        </table>
    </div>
    {:else if bothSelected && students.length === 0}
    <h6 class="text-warning">В выбранной группе нет студентов</h6>
    {:else}
    <div class='d-flex mt-2'>
        <div class="spinner-border text-white" style="width: 2rem; height: 2rem;"></div>
    </div>
    {/if}
    {/if}
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
      out:fly={{ x: 100, duration: 300 }}>
      {isSuccess ? successMessage : errorMessage}
    </div>
    {/if}
</div>