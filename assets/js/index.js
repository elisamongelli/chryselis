function openPlantDetailsDialog() {

    fetch('/html/plant-details.html')
        .then(r => r.text())
        .then(html => {
            document.body.insertAdjacentHTML('beforeend', html);
            // da qui in poi puoi usare document.getElementById('dettaglio');
            document.getElementById('plantDetailsDialog').showModal();
        });
}