document.addEventListener("DOMContentLoaded", () => {
    const selProv = document.getElementById("provincia_filter");
    const selDep  = document.getElementById("departamento_filter");
    const selLoc  = document.getElementById("localidad_filter");

    const selectedProv = selProv.dataset.selected;
    const selectedDep  = selDep.dataset.selected;
    const selectedLoc  = selLoc.dataset.selected;

    function cargarDepartamentos(provId, depSeleccionado=null) {
        selDep.innerHTML = '<option value="">Todos</option>';
        selLoc.innerHTML = '<option value="">Todas</option>';
        if (!provId) return;

        fetch(`/principal/ajax/departamentos/${provId}/`)
            .then(res => res.json())
            .then(data => {
                data.forEach(dep => {
                    const opt = document.createElement("option");
                    opt.value = dep.pk;
                    opt.text = dep.nombre;
                    if(dep.pk === depSeleccionado) opt.selected = true;
                    selDep.appendChild(opt);
                });
                if (depSeleccionado) cargarLocalidades(depSeleccionado, selectedLoc);
            });
    }

    function cargarLocalidades(depId, locSeleccionada=null) {
        selLoc.innerHTML = '<option value="">Todas</option>';
        if (!depId) return;

        fetch(`/principal/ajax/localidades/${depId}/`)
            .then(res => res.json())
            .then(data => {
                data.forEach(loc => {
                    const opt = document.createElement("option");
                    opt.value = loc.pk;
                    opt.text = loc.nombre;
                    if(loc.pk === locSeleccionada) opt.selected = true;
                    selLoc.appendChild(opt);
                });
            });
    }

    selProv.addEventListener("change", () => cargarDepartamentos(selProv.value));
    selDep.addEventListener("change", () => cargarLocalidades(selDep.value));

    // cargar seleccion inicial si hay GET
    if(selectedProv) cargarDepartamentos(selectedProv, selectedDep);
});