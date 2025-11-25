document.addEventListener("DOMContentLoaded", () => {

    const selProv = document.getElementById("provincia");
    const selDep  = document.getElementById("departamento");
    const selLoc  = document.getElementById("localidad");

    selProv.addEventListener("change", () => {
        const provId = selProv.value;
        selDep.innerHTML = '<option value="">Seleccionar departamento</option>';
        selLoc.innerHTML = '<option value="">Seleccionar localidad</option>';

        if (!provId) return;

        fetch(`/cuenta/api/departamentos/${provId}/`)
            .then(r => r.json())
            .then(data => {
                data.forEach(dep => {
                    selDep.innerHTML += `<option value="${dep.id_indec}">${dep.nombre}</option>`;
                });
            });
    });

    selDep.addEventListener("change", () => {
        const depId = selDep.value;
        selLoc.innerHTML = '<option value="">Seleccionar localidad</option>';

        if (!depId) return;

        fetch(`/cuenta/api/localidades/${depId}/`)
            .then(r => r.json())
            .then(data => {
                data.forEach(loc => {
                    selLoc.innerHTML += `<option value="${loc.id_indec}">${loc.nombre}</option>`;
                });
            });
    });
});
