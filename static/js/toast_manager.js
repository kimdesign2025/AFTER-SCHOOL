class ToastManager {
    constructor() {
        // Initialize toast container
        this.toastContainer = document.createElement('div');
        this.toastContainer.id = 'toast-container';
        this.toastContainer.className = 'w-full max-w-lg flex flex-col space-y-4 items-center';
        document.body.appendChild(this.toastContainer);
        console.log('ToastManager initialized, container appended:', this.toastContainer);

        // Inject CSS styles
        this.injectStyles();
    }

    injectStyles() {
        const styles = `
            #toast-container {
                position: fixed;
                z-index: 99999;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            }
            /* Animations pour différentes positions */
            @keyframes slide-in-top-right {
                from { transform: translate(100%, 0); opacity: 0; }
                to { transform: translate(0, 0); opacity: 1; }
            }
            @keyframes slide-out-top-right {
                from { transform: translate(0, 0); opacity: 1; }
                to { transform: translate(100%, 0); opacity: 0; }
            }
            @keyframes slide-in-top-left {
                from { transform: translate(-100%, 0); opacity: 0; }
                to { transform: translate(0, 0); opacity: 1; }
            }
            @keyframes slide-out-top-left {
                from { transform: translate(0, 0); opacity: 1; }
                to { transform: translate(-100%, 0); opacity: 0; }
            }
            @keyframes slide-in-bottom-right {
                from { transform: translate(100%, 0); opacity: 0; }
                to { transform: translate(0, 0); opacity: 1; }
            }
            @keyframes slide-out-bottom-right {
                from { transform: translate(0, 0); opacity: 1; }
                to { transform: translate(100%, 0); opacity: 0; }
            }
            @keyframes slide-in-bottom-left {
                from { transform: translate(-100%, 0); opacity: 0; }
                to { transform: translate(0, 0); opacity: 1; }
            }
            @keyframes slide-out-bottom-left {
                from { transform: translate(0, 0); opacity: 1; }
                to { transform: translate(-100%, 0); opacity: 0; }
            }
            @keyframes progress {
                from { width: 100%; }
                to { width: 0%; }
            }
            .animate-slide-in-top-right {
                animation: slide-in-top-right 0.3s ease-out forwards;
            }
            .animate-slide-out-top-right {
                animation: slide-out-top-right 0.3s ease-in forwards;
            }
            .animate-slide-in-top-left {
                animation: slide-in-top-left 0.3s ease-out forwards;
            }
            .animate-slide-out-top-left {
                animation: slide-out-top-left 0.3s ease-in forwards;
            }
            .animate-slide-in-bottom-right {
                animation: slide-in-bottom-right 0.3s ease-out forwards;
            }
            .animate-slide-out-bottom-right {
                animation: slide-out-bottom-right 0.3s ease-in forwards;
            }
            .animate-slide-in-bottom-left {
                animation: slide-in-bottom-left 0.3s ease-out forwards;
            }
            .animate-slide-out-bottom-left {
                animation: slide-out-bottom-left 0.3s ease-in forwards;
            }
            .progress-bars {
                animation: progress 4s linear forwards;
            }
        `;
        const styleSheet = document.createElement("style");
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
        console.log('Toast styles injected:', styleSheet);
    }

    setPosition(position) {
        // Supprimer les anciennes classes de position
        this.toastContainer.style.top = '';
        this.toastContainer.style.right = '';
        this.toastContainer.style.bottom = '';
        this.toastContainer.style.left = '';

        // Appliquer la nouvelle position
        switch (position) {
            case 'top-left':
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.left = '1rem';
                break;
            case 'top-right':
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.right = '1rem';
                break;
            case 'bottom-left':
                this.toastContainer.style.bottom = '1rem';
                this.toastContainer.style.left = '1rem';
                break;
            case 'bottom-right':
                this.toastContainer.style.bottom = '1rem';
                this.toastContainer.style.right = '1rem';
                break;
            default:
                this.toastContainer.style.top = '1rem';
                this.toastContainer.style.right = '1rem'; // Par défaut : top-right
        }
    }

    showToast(message, type = "info", position = "top-right") {
        const toastStyles = {
            success: {
                bg: "bg-green-100",
                border: "border-green-500",
                iconBg: "bg-green-200",
                iconColor: "text-green-600",
                titleColor: "text-green-700",
                textColor: "text-green-600",
                progressColor: "bg-green-500",
                title: gettext("Success"),
                icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`
            },
            warning: {
                bg: "bg-yellow-100",
                border: "border-yellow-500",
                iconBg: "bg-yellow-200",
                iconColor: "text-yellow-600",
                titleColor: "text-yellow-700",
                textColor: "text-yellow-600",
                progressColor: "bg-yellow-500",
                title: gettext("Warning"),
                icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 3a9 9 0 110 18 9 9 0 010-18z" /></svg>`
            },
            info: {
                bg: "bg-blue-100",
                border: "border-blue-500",
                iconBg: "bg-blue-200",
                iconColor: "text-blue-600",
                titleColor: "text-blue-700",
                textColor: "text-blue-600",
                progressColor: "bg-blue-500",
                title: gettext("Info"),
                icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M12 3a9 9 0 110 18 9 9 0 010-18z" /></svg>`
            },
            error: {
                bg: "bg-red-100",
                border: "border-red-500",
                iconBg: "bg-red-200",
                iconColor: "text-red-600",
                titleColor: "text-red-700",
                textColor: "text-red-600",
                progressColor: "bg-red-500",
                title: gettext("Error"),
                icon: `<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M12 3a9 9 0 110 18 9 9 0 010-18z" /></svg>`
            }
        };

        const style = toastStyles[type] || toastStyles.info;

        // Définir la position du conteneur
        this.setPosition(position);

        // Choisir l’animation en fonction de la position
        let slideInAnimation, slideOutAnimation;
        switch (position) {
            case 'top-left':
                slideInAnimation = 'animate-slide-in-top-left';
                slideOutAnimation = 'animate-slide-out-top-left';
                break;
            case 'top-right':
                slideInAnimation = 'animate-slide-in-top-right';
                slideOutAnimation = 'animate-slide-out-top-right';
                break;
            case 'bottom-left':
                slideInAnimation = 'animate-slide-in-bottom-left';
                slideOutAnimation = 'animate-slide-out-bottom-left';
                break;
            case 'bottom-right':
                slideInAnimation = 'animate-slide-in-bottom-right';
                slideOutAnimation = 'animate-slide-out-bottom-right';
                break;
            default:
                slideInAnimation = 'animate-slide-in-top-right';
                slideOutAnimation = 'animate-slide-out-top-right';
        }

        const toast = document.createElement("div");
        toast.className = `max-w-lg w-full ${style.bg} border-l-4 ${style.border} p-4 rounded-lg shadow-md ${slideInAnimation} relative overflow-hidden`;
        toast.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <div class="${style.iconBg} rounded-full h-8 w-8 flex items-center justify-center mr-2">
                        ${style.icon}
                    </div>
                    <div>
                        <p class="${style.titleColor} font-montserrat text-sm font-medium">${style.title}</p>
                        <p class="${style.textColor} font-montserrat text-sm">${message}</p>
                    </div>
                </div>
                <button class="text-gray-500 hover:text-gray-700 close-toast">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="absolute bottom-0 left-0 h-1 ${style.progressColor} progress-bars"></div>
        `;

        this.toastContainer.appendChild(toast);
        console.log('Toast displayed:', toast);

        const closeBtn = toast.querySelector(".close-toast");
        closeBtn.addEventListener("click", () => {
            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => toast.remove(), 300);
        });

        setTimeout(() => {
            if (toast.parentElement) {
                toast.classList.remove(slideInAnimation);
                toast.classList.add(slideOutAnimation);
                setTimeout(() => toast.remove(), 300);
            }
        }, 4000);
    }

    closeAllToasts() {
        const toasts = this.toastContainer.querySelectorAll('div');
        toasts.forEach(toast => {
            const slideInAnimation = Array.from(toast.classList).find(cls => cls.startsWith('animate-slide-in'));
            const position = slideInAnimation ? slideInAnimation.replace('animate-slide-in-', '') : 'top-right';
            const slideOutAnimation = `animate-slide-out-${position}`;

            toast.classList.remove(slideInAnimation);
            toast.classList.add(slideOutAnimation);
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.remove();
                }
            }, 300);
        });
        console.log('All toasts closed');
    }
}

// Export a singleton instance
const toastManager = new ToastManager();
window.toastManager = toastManager; // Make it globally accessible
