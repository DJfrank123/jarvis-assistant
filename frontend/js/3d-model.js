class Model3DViewer {
    constructor() {
        this.container = document.getElementById('canvas3d');
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a1a);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.z = 5;
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);
        
        // Lighting
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(5, 5, 5);
        this.scene.add(light);
        
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);
        
        // Add a default object
        this.addDefaultModel();
        
        // Start animation loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }

    addDefaultModel() {
        const geometry = new THREE.BoxGeometry(2, 2, 2);
        const material = new THREE.MeshPhongMaterial({
            color: 0xFFD700,
            emissive: 0x333333
        });
        const cube = new THREE.Mesh(geometry, material);
        this.scene.add(cube);
        this.currentModel = cube;
    }

    addRoboticHand() {
        // Clear current model
        this.scene.remove(this.currentModel);
        
        // Create robotic hand
        const group = new THREE.Group();
        
        // Wrist
        const wristGeometry = new THREE.CylinderGeometry(0.3, 0.3, 0.5, 32);
        const metalMaterial = new THREE.MeshPhongMaterial({
            color: 0xc0c0c0,
            shininess: 100
        });
        const wrist = new THREE.Mesh(wristGeometry, metalMaterial);
        group.add(wrist);
        
        // Fingers
        for (let i = 0; i < 5; i++) {
            const finger = this.createFinger(i);
            group.add(finger);
        }
        
        this.scene.add(group);
        this.currentModel = group;
    }

    createFinger(index) {
        const fingerGroup = new THREE.Group();
        const positions = [
            [-0.4, 0.5, 0],  // thumb
            [-0.2, 0.6, 0],  // index
            [0, 0.6, 0],     // middle
            [0.2, 0.6, 0],   // ring
            [0.4, 0.5, 0]    // pinky
        ];
        
        const [x, y, z] = positions[index];
        
        // Finger segments
        for (let j = 0; j < 3; j++) {
            const segGeometry = new THREE.CylinderGeometry(0.1, 0.1, 0.3, 16);
            const segMaterial = new THREE.MeshPhongMaterial({
                color: 0xFFD700,
                shininess: 50
            });
            const segment = new THREE.Mesh(segGeometry, segMaterial);
            segment.position.y = -0.15 * j;
            fingerGroup.add(segment);
        }
        
        fingerGroup.position.set(x, y, z);
        return fingerGroup;
    }

    createModel(type) {
        this.scene.remove(this.currentModel);
        
        switch(type.toLowerCase()) {
            case 'sphere':
                const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
                const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0x00ff00 });
                this.currentModel = new THREE.Mesh(sphereGeometry, sphereMaterial);
                break;
            
            case 'cube':
                const cubeGeometry = new THREE.BoxGeometry(2, 2, 2);
                const cubeMaterial = new THREE.MeshPhongMaterial({ color: 0xFFD700 });
                this.currentModel = new THREE.Mesh(cubeGeometry, cubeMaterial);
                break;
            
            case 'pyramid':
                const pyramidGeometry = new THREE.TetrahedronGeometry(1, 0);
                const pyramidMaterial = new THREE.MeshPhongMaterial({ color: 0xff6b6b });
                this.currentModel = new THREE.Mesh(pyramidGeometry, pyramidMaterial);
                break;
            
            case 'hand':
            case 'robotic_hand':
                this.addRoboticHand();
                return;
            
            default:
                this.addDefaultModel();
                return;
        }
        
        this.scene.add(this.currentModel);
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        
        if (this.currentModel) {
            this.currentModel.rotation.x += 0.01;
            this.currentModel.rotation.y += 0.01;
        }
        
        this.renderer.render(this.scene, this.camera);
    }

    onWindowResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight;
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
}

const model3DViewer = new Model3DViewer();
