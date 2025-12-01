document.addEventListener("DOMContentLoaded", () => {
    const selProv = document.getElementById("provincia_filter");
    const selDep  = document.getElementById("departamento_filter");
    const selLoc  = document.getElementById("localidad_filter");

    const selectedProv = selProv.dataset.selected;
    const selectedDep  = selDep.dataset.selected;
    const selectedLoc  = selLoc.dataset.selected;

    // Función para cargar departamentos
    function cargarDepartamentos(provId, depSeleccionado=null) {
        selDep.innerHTML = '<option value="">Todos</option>';
        selLoc.innerHTML = '<option value="">Todas</option>';
        if (!provId) return;

        fetch(`/ajax/departamentos/${provId}/`)
            .then(res => res.json())
            .then(data => {
                data.forEach(dep => {
                    const opt = document.createElement("option");
                    // *** CORRECCIÓN 1: Cambiar .pk a .id_indec ***
                    opt.value = dep.id_indec; 
                    opt.text = dep.nombre;
                    if(dep.id_indec === depSeleccionado) opt.selected = true;
                    selDep.appendChild(opt);
                });
                if (depSeleccionado) cargarLocalidades(depSeleccionado, selectedLoc);
            });
    }

    // Función para cargar localidades
    function cargarLocalidades(depId, locSeleccionada=null) {
        selLoc.innerHTML = '<option value="">Todas</option>';
        if (!depId) return;

        fetch(`/ajax/localidades/${depId}/`)
            .then(res => res.json())
            .then(data => {
                data.forEach(loc => {
                    const opt = document.createElement("option");
                    // *** CORRECCIÓN 2: Cambiar .pk a .id_indec ***
                    opt.value = loc.id_indec;
                    opt.text = loc.nombre;
                    if(loc.id_indec === locSeleccionada) opt.selected = true;
                    selLoc.appendChild(opt);
                });
            });
    }

    // Manejadores de eventos
    selProv.addEventListener("change", () => cargarDepartamentos(selProv.value));
    selDep.addEventListener("change", () => cargarLocalidades(selDep.value));

    // Carga inicial al refrescar la página
    if(selectedProv) cargarDepartamentos(selectedProv, selectedDep);
});