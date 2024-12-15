document.addEventListener("DOMContentLoaded", () => {
    // Validasi Upload Form
    const uploadForm = document.querySelector("#upload-form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", (event) => {
            const imageDataset = document.querySelector("#image_dataset").files[0];
            const audioDataset = document.querySelector("#audio_dataset").files[0];
            const mapper = document.querySelector("#mapper").files[0];

            if (!imageDataset || !audioDataset || !mapper) {
                event.preventDefault();
                alert("Please upload all required files!");
            }
        });
    }

    // Animasi Navigasi
    const navLinks = document.querySelectorAll("nav a");
    navLinks.forEach((link) => {
        link.addEventListener("mouseover", () => {
            link.style.color = "#27ae60";
        });
        link.addEventListener("mouseout", () => {
            link.style.color = "";
        });
    });
});
