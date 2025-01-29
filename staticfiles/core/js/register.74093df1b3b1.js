const imageInput = document.getElementById('id_image');
const imageContainer = document.getElementById('imageContainer');
const mainCanvas = document.getElementById('mainCanvas');
const mainCtx = mainCanvas.getContext('2d');
const cropCanvas = document.getElementById('cropCanvas');
const cropCtx = cropCanvas.getContext('2d');
const croppedImageDataInput = document.getElementById('croppedImageData');

let uploadedImage = null;
let cropSize = 100; // Default crop size, will be updated dynamically
let cropX = 50;
let cropY = 50;
let isDragging = false;

imageInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = (e) => {
            const img = new Image();
            img.src = e.target.result;

            img.onload = () => {
                document.getElementById('image-container').style.display='flex';
                uploadedImage = img;
                // Calculate the dimensions to fit within the container
                const containerWidth = imageContainer.clientWidth;
                const containerHeight = imageContainer.clientHeight;

                const scale = Math.min(
                    containerWidth / img.width,
                    containerHeight / img.height
                );

                const scaledWidth = img.width * scale;
                const scaledHeight = img.height * scale;

                // Set the canvas size to match scaled dimensions
                mainCanvas.width = scaledWidth;
                mainCanvas.height = scaledHeight;

                // Draw the scaled image on the canvas
                mainCtx.clearRect(0, 0, scaledWidth, scaledHeight);
                mainCtx.drawImage(img, 0, 0, scaledWidth, scaledHeight);

                // Update crop size (shorter side of the image)
                cropSize = Math.min(scaledWidth, scaledHeight);
                cropCanvas.width = cropSize;
                cropCanvas.height = cropSize;

                // Initial crop box position
                cropX = (scaledWidth - cropSize) / 2;
                cropY = (scaledHeight - cropSize) / 2;
    

                drawCropBox();
            };
        };

        reader.readAsDataURL(file);
    }
});
function submit_to_crop(){
     // Draw the cropped area on the crop canvas
     cropCtx.clearRect(0, 0, cropSize, cropSize);
        cropCtx.drawImage(
            uploadedImage,
            cropX / (mainCanvas.width / uploadedImage.width),
            cropY / (mainCanvas.height / uploadedImage.height),
            cropSize / (mainCanvas.width / uploadedImage.width),
            cropSize / (mainCanvas.height / uploadedImage.height),
            0,
            0,
            cropSize,
            cropSize
        );
        
        // Update hidden input with the cropped image data (base64)
        const croppedImageData = cropCanvas.toDataURL();
        croppedImageDataInput.value = croppedImageData;
    document.getElementById('image-container').style.display='none';
}

function drawCropBox() {
    if (!uploadedImage) return;

    
    // Redraw the image
    mainCtx.clearRect(0, 0, mainCanvas.width, mainCanvas.height);
    mainCtx.drawImage(uploadedImage, 0, 0, mainCanvas.width, mainCanvas.height);

    // Draw the crop box
    mainCtx.strokeStyle = "red";
    mainCtx.lineWidth = 2;
    mainCtx.strokeRect(cropX, cropY, cropSize, cropSize);
}

mainCanvas.addEventListener('mousedown', (event) => {
    const rect = mainCanvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    if (
        x >= cropX &&
        x <= cropX + cropSize &&
        y >= cropY &&
        y <= cropY + cropSize
    ) {
        isDragging = true;
    }
});

mainCanvas.addEventListener('mousemove', (event) => {
    if (isDragging) {
        const rect = mainCanvas.getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;

        cropX = Math.max(0, Math.min(x - cropSize / 2, mainCanvas.width - cropSize));
        cropY = Math.max(0, Math.min(y - cropSize / 2, mainCanvas.height - cropSize));

        drawCropBox();
    }
});

mainCanvas.addEventListener('mouseup', () => {
    if (isDragging) {
        isDragging = false;

       
    }
});

mainCanvas.addEventListener('mouseleave', () => {
    isDragging = false;
});

// Ensure that the form submits the cropped image as well
document.getElementById('imageForm').addEventListener('submit', function(event) {
    if (!croppedImageDataInput.value && imageInput.value) {
        alert("Please try selecting image again!");
        event.preventDefault(); 
    }
    
});