var setVanta = () => {
	if (window.VANTA)
		window.VANTA.NET({
			el: '#background',
			mouseControls: false,
			touchControls: true,
			gyroControls: true,
			scale: 1,
			scaleMobile: 1.0,
			color: 0xffffff,
			backgroundColor: 0x0,
			points: 20.0,
			spacing: 30.0,
			maxDistance: 10.0
		})
}
document.addEventListener('DOMContentLoaded', function () {
	setVanta()
})
