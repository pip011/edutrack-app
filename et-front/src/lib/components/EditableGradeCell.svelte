<script>
    export let value = null;    
    export let studentId;          
    export let day;           
    export let subjectId;         
    export let month;               
    export let year;                
    export let onSave;            

    const gradeColors = {
      2: "text-danger",   
      3: "text-warning",   
      4: "text-info",   
      5: "text-success"    
    };

    let grade = value;

    function handleInput(e) {
        let v = e.target.value ? parseInt(e.target.value) : null;

        if (v !== null) {
          if (![2, 3, 4, 5].includes(v)) v = 2
        }

        grade = v;
    }

    function handleBlur() {
        onSave({ studentId, day, grade, subjectId, month, year });
    }
</script>

<td>
  <input 
    type="text" 
    min="2" 
    max="5"
    bind:value={grade}
    on:input={handleInput}
    on:blur={handleBlur}
    class={gradeColors[grade] ?? ""}
    style="
      all: unset;
      width: 100%;
      height: 100%;
      text-align: center;
      box-sizing: border-box;
      cursor: pointer;"/>
</td>