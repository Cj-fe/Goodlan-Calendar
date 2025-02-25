const NotificationManager = {
    mobileNotificationCount: 0,
    maxMobileNotifications: 2,
    isMobile: () => window.innerWidth <= 768,

    showNotification: function (type, message) {
        if (this.isMobile() && this.mobileNotificationCount >= this.maxMobileNotifications) {
            const notifications = document.querySelectorAll('.bootstrap-notify-container');
            if (notifications.length > 0) {
                notifications[0].remove();
                this.mobileNotificationCount--;
            }
        }

        if (this.isMobile()) {
            this.mobileNotificationCount++;
        }

        $.notify({
            message: message,
            icon: type === 'success' ? 'bi bi-check-circle' : 'bi bi-exclamation-circle'
        }, {
            type: type,
            allow_dismiss: true,
            newest_on_top: true,
            timer: 3000,
            placement: {
                from: 'top',
                align: this.isMobile() ? 'center' : 'right'
            },
            animate: {
                enter: 'animated bounceInDown',
                exit: 'animated bounceOutUp'
            },
            template:
                '<div data-notify="container" class="bootstrap-notify-container alert alert-{0}" role="alert">' +
                '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                '<div class="notification-content">' +
                '<span data-notify="icon"></span>' +
                '<span data-notify="message">{2}</span>' +
                '</div>' +
                '</div>',
            onClose: () => {
                if (this.isMobile()) {
                    this.mobileNotificationCount--;
                }
            }
        });
    }
};