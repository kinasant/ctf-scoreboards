if (window.location.pathname === "/register") {
	let targetForm = document.forms[0];
	let url = new URL(targetForm.action);
	if (url.pathname === "/register" && targetForm.id != "site_password_form") {
		var onSubmit = function (token) {
			targetForm.submit();
		};
		function registerValidate(event) {
			event.preventDefault();
			if (!targetForm.checkValidity()) {
				targetForm.reportValidity();
			} else {
				grecaptcha.execute();
			}
		}
		let targetBtn = targetForm.querySelector('[type="submit"]');
		targetBtn.insertAdjacentHTML(
			"beforebegin",
			`<div id="recaptcha" class="g-recaptcha" data-sitekey="6LcQsq4UAAAAANMoNqPRyCLJXymW2_0Ol9JDI03h" data-callback="onSubmit" data-size="invisible"></div>`,
		);
		targetBtn.onclick = registerValidate;
	}
}