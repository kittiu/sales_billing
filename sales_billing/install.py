import click

from sales_billing.setup import after_install as setup


def after_install():
	try:
		print("Setting up Sales Billing...")
		setup()

		click.secho("Thank you for installing Sales Billing!", fg="green")

	except Exception as e:
		BUG_REPORT_URL = "https://github.com/kittiu/sales_billing/issues/new"
		click.secho(
			"Installation for Sales Billing app failed due to an error."
			" Please try re-installing the app or"
			f" report the issue on {BUG_REPORT_URL} if not resolved.",
			fg="bright_red",
		)
		raise e
