document.addEventListener("DOMContentLoaded", () => {

    const prov = document.getElementById("provincia");
    const dep = document.getElementById("departamento");
    const loc = document.getElementById("localidad");

    prov.addEventListener("change", () => {
        const provId = prov.value;

        dep.innerHTML = '<option value="">Todos</option>';
        loc.innerHTML = '<option value="">Todos</option>';

        if (!provId) return;

        fetch(`/cuenta/api/departamentos/${provId}/`)
            .then(res => res.json())
            .then(data => {
                dep.innerHTML = '<option value="">Todos</option>';
                data.forEach(d => {
                    dep.innerHTML += `<option value="${d.pk}">${d.nombre}</option>`;
                });
            });
    });

    dep.addEventListener("change", () => {
        const depId = dep.value;

        loc.innerHTML = '<option value="">Todos</option>';

        if (!depId) return;

        fetch(`/cuenta/api/localidades/${depId}/`)
            .then(res => res.json())
            .then(data => {
                loc.innerHTML = '<option value="">Todas</option>';
                data.forEach(l => {
                    loc.innerHTML += `<option value="${l.pk}">${l.nombre}</option>`;
                });
            });

    });
});