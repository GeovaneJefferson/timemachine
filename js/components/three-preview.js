export class ThreePreview {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.model = null;
        this.animationId = null;
        this.isRotating = true;
    }

    async init(containerId, fileUrl, fileType) {
        try {
            // Dynamically import Three.js
            const THREE = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/build/three.module.js');
            
            // Initialize scene
            const container = document.getElementById(containerId);
            if (!container) return false;
            
            // Clear existing content
            container.innerHTML = '';
            
            // Create scene
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(0x1a1a1a);
            
            // Create camera
            this.camera = new THREE.PerspectiveCamera(
                45,
                container.clientWidth / container.clientHeight,
                0.1,
                1000
            );
            this.camera.position.set(5, 5, 5);
            
            // Create renderer
            this.renderer = new THREE.WebGLRenderer({ 
                antialias: true, 
                alpha: true,
                preserveDrawingBuffer: true
            });
            this.renderer.setSize(container.clientWidth, container.clientHeight);
            this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            this.renderer.shadowMap.enabled = true;
            container.appendChild(this.renderer.domElement);
            
            // Add lighting
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            this.scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(10, 10, 10);
            directionalLight.castShadow = true;
            this.scene.add(directionalLight);
            
            // Add OrbitControls
            try {
                const { OrbitControls } = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/controls/OrbitControls.js');
                this.controls = new OrbitControls(this.camera, this.renderer.domElement);
                this.controls.enableDamping = true;
                this.controls.dampingFactor = 0.05;
                this.controls.screenSpacePanning = false;
                this.controls.minDistance = 1;
                this.controls.maxDistance = 100;
                this.controls.maxPolarAngle = Math.PI;
            } catch (e) {
                console.warn('OrbitControls not available:', e);
            }
            
            // Add grid helper
            const gridHelper = new THREE.GridHelper(10, 10, 0x444444, 0x888888);
            gridHelper.position.y = -2;
            this.scene.add(gridHelper);
            
            // Add axes helper
            const axesHelper = new THREE.AxesHelper(5);
            this.scene.add(axesHelper);
            
            // Load the model
            await this.loadModel(fileUrl, fileType, THREE);
            
            // Start animation loop
            this.animate();
            
            // Handle window resize
            this.handleResize = () => this.onWindowResize(container);
            window.addEventListener('resize', this.handleResize);
            
            // Add click event for container
            this.container = container;
            
            return true;
            
        } catch (error) {
            console.error('Failed to initialize Three.js preview:', error);
            this.showError(containerId);
            return false;
        }
    }
    
    async loadModel(url, fileType, THREE) {
        try {
            let loader;
            
            if (fileType === 'glb' || fileType === 'gltf') {
                const { GLTFLoader } = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/loaders/GLTFLoader.js');
                loader = new GLTFLoader();
                
                loader.load(url, (gltf) => {
                    this.model = gltf.scene;
                    this.scene.add(this.model);
                    
                    // Enable shadows for all meshes
                    this.model.traverse((child) => {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });
                    
                    // Center the model
                    const box = new THREE.Box3().setFromObject(this.model);
                    const center = box.getCenter(new THREE.Vector3());
                    const size = box.getSize(new THREE.Vector3());
                    
                    // Center the model
                    this.model.position.x -= center.x;
                    this.model.position.y -= center.y;
                    this.model.position.z -= center.z;
                    
                    // Adjust camera to fit the model
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const fov = this.camera.fov * (Math.PI / 180);
                    let cameraZ = Math.abs(maxDim / Math.sin(fov / 2));
                    
                    // Adjust for perspective
                    cameraZ *= 1.5;
                    this.camera.position.set(cameraZ, cameraZ, cameraZ);
                    this.camera.lookAt(0, 0, 0);
                    
                    if (this.controls) {
                        this.controls.target.set(0, 0, 0);
                        this.controls.update();
                    }
                    
                    console.log(`Loaded ${fileType.toUpperCase()} model:`, this.model);
                    
                }, 
                // Progress callback
                (xhr) => {
                    console.log(`${(xhr.loaded / xhr.total * 100)}% loaded`);
                },
                // Error callback
                (error) => {
                    console.error('GLTF/GLB load error:', error);
                    this.showError();
                });
                
            } else if (fileType === 'fbx') {
                const { FBXLoader } = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/loaders/FBXLoader.js');
                loader = new FBXLoader();
                
                loader.load(url, (fbx) => {
                    this.model = fbx;
                    this.scene.add(this.model);
                    
                    // Enable shadows for all meshes
                    this.model.traverse((child) => {
                        if (child.isMesh) {
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });
                    
                    // Center the model
                    const box = new THREE.Box3().setFromObject(this.model);
                    const center = box.getCenter(new THREE.Vector3());
                    this.model.position.sub(center);
                    
                    // Adjust camera
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const fov = this.camera.fov * (Math.PI / 180);
                    let cameraZ = Math.abs(maxDim / Math.sin(fov / 2)) * 1.5;
                    
                    this.camera.position.set(cameraZ, cameraZ, cameraZ);
                    this.camera.lookAt(0, 0, 0);
                    
                    if (this.controls) {
                        this.controls.target.set(0, 0, 0);
                        this.controls.update();
                    }
                    
                    console.log('Loaded FBX model:', this.model);
                    
                }, undefined, (error) => {
                    console.error('FBX load error:', error);
                    this.showError();
                });
            } else if (fileType === 'obj') {
                const { OBJLoader } = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/loaders/OBJLoader.js');
                loader = new OBJLoader();
                
                loader.load(url, (obj) => {
                    this.model = obj;
                    this.scene.add(this.model);
                    
                    // Add basic material to all meshes
                    this.model.traverse((child) => {
                        if (child.isMesh) {
                            child.material = new THREE.MeshStandardMaterial({ 
                                color: 0x888888,
                                roughness: 0.7,
                                metalness: 0.2
                            });
                            child.castShadow = true;
                            child.receiveShadow = true;
                        }
                    });
                    
                    // Center the model
                    const box = new THREE.Box3().setFromObject(this.model);
                    const center = box.getCenter(new THREE.Vector3());
                    this.model.position.sub(center);
                    
                    // Adjust camera
                    const size = box.getSize(new THREE.Vector3());
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const fov = this.camera.fov * (Math.PI / 180);
                    let cameraZ = Math.abs(maxDim / Math.sin(fov / 2)) * 1.5;
                    
                    this.camera.position.set(cameraZ, cameraZ, cameraZ);
                    this.camera.lookAt(0, 0, 0);
                    
                    if (this.controls) {
                        this.controls.target.set(0, 0, 0);
                        this.controls.update();
                    }
                    
                    console.log('Loaded OBJ model:', this.model);
                    
                }, undefined, (error) => {
                    console.error('OBJ load error:', error);
                    this.showError();
                });
            } else if (fileType === 'stl') {
                const { STLLoader } = await import('https://cdn.jsdelivr.net/npm/three@0.149.0/examples/jsm/loaders/STLLoader.js');
                loader = new STLLoader();
                
                loader.load(url, (geometry) => {
                    const material = new THREE.MeshStandardMaterial({ 
                        color: 0x888888,
                        roughness: 0.7,
                        metalness: 0.2
                    });
                    this.model = new THREE.Mesh(geometry, material);
                    this.scene.add(this.model);
                    
                    this.model.castShadow = true;
                    this.model.receiveShadow = true;
                    
                    // Center the model
                    geometry.computeBoundingBox();
                    const box = geometry.boundingBox;
                    const center = new THREE.Vector3();
                    box.getCenter(center);
                    this.model.position.sub(center);
                    
                    // Adjust camera
                    const size = new THREE.Vector3();
                    box.getSize(size);
                    const maxDim = Math.max(size.x, size.y, size.z);
                    const fov = this.camera.fov * (Math.PI / 180);
                    let cameraZ = Math.abs(maxDim / Math.sin(fov / 2)) * 1.5;
                    
                    this.camera.position.set(cameraZ, cameraZ, cameraZ);
                    this.camera.lookAt(0, 0, 0);
                    
                    if (this.controls) {
                        this.controls.target.set(0, 0, 0);
                        this.controls.update();
                    }
                    
                    console.log('Loaded STL model:', this.model);
                    
                }, undefined, (error) => {
                    console.error('STL load error:', error);
                    this.showError();
                });
            }
            
        } catch (error) {
            console.error('Failed to load 3D model:', error);
            this.showError();
        }
    }
    
    showError(containerId = null) {
        if (containerId && document.getElementById(containerId)) {
            const container = document.getElementById(containerId);
            container.innerHTML = `
                <div class="flex flex-col items-center justify-center h-full">
                    <span class="material-icons-round text-4xl text-[var(--color-status-error)] mb-2">error</span>
                    <p class="text-sm text-[var(--color-text-secondary)] text-center">Failed to load 3D model</p>
                    <p class="text-xs text-[var(--color-text-secondary)] text-center mt-1">Format not supported or file corrupted</p>
                </div>
            `;
        }
        
        // Also show a simple error cube in the scene if we have THREE
        if (this.scene) {
            try {
                const errorGeometry = new THREE.BoxGeometry(1, 1, 1);
                const errorMaterial = new THREE.MeshBasicMaterial({ color: 0xff0000, wireframe: true });
                this.model = new THREE.Mesh(errorGeometry, errorMaterial);
                this.scene.add(this.model);
            } catch (e) {
                console.error('Could not create error mesh:', e);
            }
        }
    }
    
    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        if (this.model && this.isRotating) {
            this.model.rotation.y += 0.005;
        }
        
        if (this.controls) {
            this.controls.update();
        }
        
        if (this.renderer && this.scene && this.camera) {
            this.renderer.render(this.scene, this.camera);
        }
    }
    
    toggleRotation() {
        this.isRotating = !this.isRotating;
    }
    
    onWindowResize(container) {
        if (!this.camera || !this.renderer || !container) return;
        
        this.camera.aspect = container.clientWidth / container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(container.clientWidth, container.clientHeight);
    }
    
    dispose() {
        // Stop animation loop
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        
        // Remove event listeners
        if (this.handleResize) {
            window.removeEventListener('resize', this.handleResize);
            this.handleResize = null;
        }
        
        // Dispose Three.js objects
        if (this.model && this.model.traverse) {
            this.model.traverse((object) => {
                if (object.geometry) object.geometry.dispose();
                if (object.material) {
                    if (object.material.map) object.material.map.dispose();
                    if (Array.isArray(object.material)) {
                        object.material.forEach(material => material.dispose());
                    } else {
                        object.material.dispose();
                    }
                }
            });
        }
        
        if (this.controls) {
            this.controls.dispose();
            this.controls = null;
        }
        
        if (this.renderer) {
            this.renderer.dispose();
            this.renderer.forceContextLoss();
            const canvas = this.renderer.domElement;
            if (canvas && canvas.parentNode) {
                canvas.parentNode.removeChild(canvas);
            }
            this.renderer = null;
        }
        
        // Clear references
        this.scene = null;
        this.camera = null;
        this.model = null;
        this.container = null;
        
        console.log('ThreePreview disposed');
    }
}