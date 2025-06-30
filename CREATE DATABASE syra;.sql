CREATE DATABASE syra;
USE syra;


CREATE TABLE personal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    usuario VARCHAR(50) NOT NULL,
    contrasena VARCHAR(50) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    tipo_usuario VARCHAR(50) NOT NULL
);


CREATE TABLE paciente (
    id_paciente INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido_paterno VARCHAR(50) NOT NULL,
    apellido_materno VARCHAR(50) NOT NULL,
    direccion VARCHAR(50) NOT NULL,
    telefono VARCHAR(50) NOT NULL,
    nss VARCHAR(50) NOT NULL,
    temperatura VARCHAR(50) NOT NULL,
    peso VARCHAR(50) NOT NULL,
    edad VARCHAR(50) NOT NULL,
    talla VARCHAR(50) NOT NULL,
    id_personal INT NOT NULL,
    FOREIGN KEY (id_personal) REFERENCES personal(id)
);


CREATE TABLE cita (
    id_cita INT PRIMARY KEY AUTO_INCREMENT,
    id_paciente INT NOT NULL,
    hora TIME NOT NULL,
    fecha DATE NOT NULL,
    motivo VARCHAR(50) NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente)
);








-- Personal médico
INSERT INTO personal (nombre, usuario, contrasena, telefono, tipo_usuario)
VALUES ('Dr. José Parra', 'admin', 'admin', '555-123-4567', 'medico');

-- Personal recepcionista
INSERT INTO personal (nombre, usuario, contrasena, telefono, tipo_usuario)
VALUES ('Lucía Ramírez', 'admin2', 'admin2', '555-987-6543', 'recepcionista');



INSERT INTO paciente (nombre, direccion, telefono, nss, temperatura, peso, edad, talla, id_personal)
VALUES 
('Juan Pérez', 'Calle A 123', '555-111-2222', 'NSS001', 36.5, 70.0, 30, 1.75, 1),
('María López', 'Calle B 456', '555-222-3333', 'NSS002', 37.0, 60.0, 25, 1.65, 1),
('Carlos García', 'Calle C 789', '555-333-4444', 'NSS003', 38.2, 80.0, 40, 1.80, 1),
('Ana Torres', 'Calle D 321', '555-444-5555', 'NSS004', 36.7, 55.0, 22, 1.60, 1),
('Luis Mendoza', 'Calle E 654', '555-555-6666', 'NSS005', 37.5, 90.0, 50, 1.78, 1);





INSERT INTO cita (id_paciente, hora, fecha, motivo)
VALUES 
(1, '09:00:00', CURDATE() - INTERVAL 1 DAY, 'Consulta general'),
(2, '10:30:00', CURDATE() - INTERVAL 1 DAY, 'Dolor de cabeza'),
(3, '13:00:00', CURDATE() - INTERVAL 1 DAY, 'Dolor abdominal');


INSERT INTO cita (id_paciente, hora, fecha, motivo)
VALUES 
(4, '08:30:00', CURDATE() - INTERVAL 2 DAY, 'Chequeo de rutina'),
(5, '11:15:00', CURDATE() - INTERVAL 2 DAY, 'Presión alta'),
(1, '15:00:00', CURDATE() - INTERVAL 2 DAY, 'Resultados de laboratorio');
