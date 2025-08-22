<?php
header('Content-Type: application/json');

$response = ["success" => false, "message" => ""];

// Define la misma contraseña que en admin.html
$adminPassword = "tu-contraseña-secreta"; // 👈 CAMBIA ESTO

// Verificación de la contraseña para un acceso seguro
if (!isset($_POST['password']) || $_POST['password'] !== $adminPassword) {
    $response['message'] = 'Acceso denegado. Contraseña incorrecta.';
    echo json_encode($response);
    exit;
}

$upload_dir = "assets/images/";
if (!is_dir($upload_dir)) {
    $response['message'] = "Error: La carpeta 'assets/images/' no existe.";
    echo json_encode($response);
    exit;
}

// Validaciones del archivo
if (!isset($_FILES["imageFile"]) || $_FILES["imageFile"]["error"] !== UPLOAD_ERR_OK) {
    $response['message'] = "Error al subir el archivo.";
    echo json_encode($response);
    exit;
}

$file_name = basename($_FILES["imageFile"]["name"]);
$imageFileType = strtolower(pathinfo($file_name, PATHINFO_EXTENSION));
$new_file_name = uniqid() . "_" . $file_name;
$target_file = $upload_dir . $new_file_name;

$check = getimagesize($_FILES["imageFile"]["tmp_name"]);
if($check === false) {
    $response['message'] = "El archivo no es una imagen.";
    echo json_encode($response);
    exit;
}

if ($_FILES["imageFile"]["size"] > 5000000) { // 5MB
    $response['message'] = "El archivo es demasiado grande (máx. 5MB).";
    echo json_encode($response);
    exit;
}

if($imageFileType != "jpg" && $imageFileType != "png" && $imageFileType != "jpeg") {
    $response['message'] = "Solo se permiten archivos JPG, JPEG y PNG.";
    echo json_encode($response);
    exit;
}

// Mueve el archivo a la carpeta de imágenes
if (move_uploaded_file($_FILES["imageFile"]["tmp_name"], $target_file)) {
    // Actualiza el archivo JSON
    $jsonFile = 'images.json';
    if (file_exists($jsonFile)) {
        $jsonData = json_decode(file_get_contents($jsonFile), true);
        
        $imageKey = $_POST['imageKey'];
        
        // Opcional: Elimina la imagen antigua para liberar espacio
        if (isset($jsonData[$imageKey]) && file_exists($jsonData[$imageKey]) && $jsonData[$imageKey] !== $target_file) {
            unlink($jsonData[$imageKey]);
        }
        
        $jsonData[$imageKey] = $target_file;
        
        if (file_put_contents($jsonFile, json_encode($jsonData, JSON_PRETTY_PRINT))) {
            $response['success'] = true;
            $response['message'] = "¡Éxito! La imagen se subió y el sitio web se actualizó.";
        } else {
            $response['message'] = "La imagen se subió, pero no se pudo actualizar el archivo JSON.";
        }
    } else {
        $response['message'] = "Error: El archivo 'images.json' no se encontró.";
    }
} else {
    $response['message'] = "Hubo un error al subir el archivo. Inténtalo de nuevo.";
}

echo json_encode($response);
?>