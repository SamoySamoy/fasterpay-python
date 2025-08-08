import requests
import json


class Einvoice:
    def __init__(self, gateway):
        self.gateway = gateway
        self.api_url = gateway.config.external_api_url
        self.api_key = gateway.config.private_key

    def create_invoice(self, params: dict) -> dict:
        """
        Create a new E-Invoice.

        Automatically switches to multipart/form-data if `template.logo` or `items.product.image` contains a file object.

        Docs:
            https://docs.fasterpay.com/api#section-create-invoice

        Returns:
            dict: API response containing invoice data.
        """
        if not params.get("contact_id"):
            raise ValueError("'contact_id' is required.")
        if not params.get("currency"):
            raise ValueError("'currency' is required.")
        if not params.get("items") or not isinstance(params["items"], list):
            raise ValueError("'items' must be a non-empty list of item objects.")
        if params.get("template") and params.get("invoice_template_id"):
            raise ValueError("Provide either 'template' or 'invoice_template_id', not both.")

        url = f"{self.api_url}/api/external/invoices"
        headers = {"X-ApiKey": self.api_key}

        # Check for file uploads
        files = {}
        file_keys = []

        if isinstance(params.get("template", {}).get("logo"), (bytes, tuple)):
            files["template.logo"] = params["template"]["logo"]
            params["template"]["logo"] = None  # Replace file with placeholder
            file_keys.append("template.logo")

        for i, item in enumerate(params.get("items", [])):
            product = item.get("product")
            if isinstance(product, dict) and isinstance(product.get("image"), (bytes, tuple)):
                field_name = f"items[{i}].product.image"
                files[field_name] = product["image"]
                product["image"] = None  # Replace with placeholder
                file_keys.append(field_name)

        if files:
            # Send as multipart/form-data
            headers.pop("Content-Type", None)
            form_data = {
                "json": json.dumps(params)
            }
            response = requests.post(url, headers=headers, data=form_data, files=files)
        else:
            # Send as JSON
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()

    def list_invoices(self, params: dict = None) -> dict:
        """
        List E-Invoices with optional filters.

        Returns:
            dict: Response data from the API.
        """
        url = f"{self.api_url}/api/external/invoices"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, params=params or {}, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_invoice(self, invoice_id: str, params: dict = None) -> dict:
        """
        Retrieve details of a specific E-Invoice by ID.

        Returns:
            dict: Invoice details.
        """
        if not invoice_id:
            raise ValueError("invoice_id is required.")

        url = f"{self.api_url}/api/external/invoices/{invoice_id}"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }
        response = requests.get(url, params=params or {}, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def update_invoice(self, invoice_id: str, params: dict) -> dict:
        """
        Update an existing E-Invoice.

        Automatically switches to multipart/form-data if `template.logo` or `items.product.image` contains a file object.

        Docs:
            https://docs.fasterpay.com/api#section-update-invoice

        Args:
            invoice_id (str): The ID of the invoice to update.
            params (dict): Fields to update.

        Returns:
            dict: API response.
        """
        if not invoice_id:
            raise ValueError("invoice_id is required.")
        if not isinstance(params, dict):
            raise ValueError("params must be a dictionary.")

        url = f"{self.api_url}/api/external/invoices/{invoice_id}"
        headers = {"X-ApiKey": self.api_key}

        # Check for file uploads
        files = {}
        file_keys = []

        if isinstance(params.get("template", {}).get("logo"), (bytes, tuple)):
            files["template.logo"] = params["template"]["logo"]
            params["template"]["logo"] = None
            file_keys.append("template.logo")

        for i, item in enumerate(params.get("items", [])):
            product = item.get("product")
            if isinstance(product, dict) and isinstance(product.get("image"), (bytes, tuple)):
                field_name = f"items[{i}].product.image"
                files[field_name] = product["image"]
                product["image"] = None
                file_keys.append(field_name)

        if files:
            # multipart/form-data (use POST method)
            form_data = {
                "json": json.dumps(params)
            }
            response = requests.post(url, headers=headers, data=form_data, files=files)
        else:
            # Standard PUT request
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()
    
    def update_invoice_status(self, invoice_id: str, status: str) -> dict:
        """
        Update the status of an existing E-Invoice.

        Allowed status values:
            - void
            - uncollectible

        Docs:
            https://docs.fasterpay.com/api#section-update-invoice-status

        Args:
            invoice_id (str): ID of the invoice to update.
            status (str): New status value. Must be one of "void" or "uncollectible".

        Returns:
            dict: API response with updated invoice data.
        """
        if not invoice_id:
            raise ValueError("invoice_id is required.")
        if status not in ["void", "uncollectible"]:
            raise ValueError("Invalid status. Must be one of: 'void', 'uncollectible'.")

        url = f"{self.api_url}/api/external/invoices/{invoice_id}/status"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {"status": status}
        response = requests.put(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def preview_invoice_pdf(self, invoice_id: str) -> str:
        """
        Generate an HTML preview of the invoice's PDF version.

        Docs:
            https://docs.fasterpay.com/api#section-preview-invoice

        Args:
            invoice_id (str): The ID of the invoice to preview.

        Returns:
            str: Raw HTML content of the invoice preview.
        """
        if not invoice_id:
            raise ValueError("invoice_id is required.")

        url = f"{self.api_url}/api/external/invoices/{invoice_id}/pdf"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text  # Returns HTML content 
    

    def send_invoice(self, invoice_id: str, test: bool = False) -> dict:
        """
        Send the invoice to the customer's email address.
        
        Optionally sends a test invoice to the merchant’s email.

        Args:
            invoice_id (str): The ID of the invoice to send.
            test (bool): If True, sends a test invoice to the merchant email.

        Returns:
            dict: API response containing the invoice data.
        """
        if not invoice_id:
            raise ValueError("invoice_id is required.")

        url = f"{self.api_url}/api/external/invoices/{invoice_id}/send"
        headers = {
            "X-ApiKey": self.api_key,
            "Content-Type": "application/json"
        }

        data = {"test": test} if test else {}

        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_invoice_template(self, template: dict) -> dict:
        """
        Create a new invoice template.

        Automatically switches to multipart/form-data if `logo` is a file.

        Args:
            template (dict): Dictionary containing template parameters:
                - name (str): Required. Template name.
                - country_code (str): Required. 2-letter country code.
                - footer (str): Optional. Footer text.
                - address (str) or localized_address (dict): Only one allowed.
                - colors (dict): Required. Must include 'primary' and 'secondary' hex colors.
                - logo (file-like or bytes, optional): Logo file if provided.

        Returns:
            dict: API response containing created template details.
        """
        if not template.get("name"):
            raise ValueError("'name' is required.")
        if not template.get("country_code"):
            raise ValueError("'country_code' is required.")
        if not template.get("colors"):
            raise ValueError("'colors' is required and must contain 'primary' and 'secondary'.")

        if template.get("address") and template.get("localized_address"):
            raise ValueError("Provide either 'address' or 'localized_address', not both.")

        url = f"{self.api_url}/api/external/invoices/templates"
        headers = {"X-ApiKey": self.api_key}

        files = {}
        logo = template.get("logo")
        if isinstance(logo, (bytes, tuple)):
            files["logo"] = logo
            template["logo"] = None  # Remove file object from JSON

        if files:
            # Multipart form-data required
            headers.pop("Content-Type", None)
            form_data = {
                "json": json.dumps(template)
            }
            response = requests.post(url, headers=headers, data=form_data, files=files)
        else:
            # Pure JSON
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=template)

        response.raise_for_status()
        return response.json()
    
    def list_invoice_templates(self, params: dict = None) -> dict:
        """
        Retrieve a list of all invoice templates with optional filters.

        Args:
            params (dict, optional): Query parameters:
                - page (int): Page number (starting from 1)
                - per_page (int): Number of records per page (max 1000)
                - filter (dict): Optional nested filter, e.g.:
                    - name (str): Filter by template name

        Returns:
            dict: Response data containing list of invoice templates
        """
        url = f"{self.api_url}/api/external/invoices/templates"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers, params=params or {})
        response.raise_for_status()
        return response.json()
    
    def get_invoice_template(self, template_id: str) -> dict:
        """
        Retrieve details of a specific invoice template by ID.

        Args:
            template_id (str): The ID of the invoice template to retrieve.

        Returns:
            dict: API response containing the template details.
        """
        if not template_id:
            raise ValueError("template_id is required.")

        url = f"{self.api_url}/api/external/invoices/templates/{template_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_invoice_template(self, template_id: str, params: dict) -> dict:
        """
        Update an existing invoice template.

        - Uses POST with `_method: PUT` if a logo file is included.
        - Otherwise, uses a standard PUT request.

        Endpoint:
            PUT (or POST with _method=PUT if files present)
            https://business.fasterpay.com/api/external/invoices/templates/{template_id}

        Args:
            template_id (str): ID of the template to update.
            params (dict): Fields to update. Possible keys:
                - name (str), address (str), country_code (str),
                - footer (str), localized_address (dict), colors (dict),
                - logo (file-like object, optional)

        Returns:
            dict: API response with updated template data.
        """
        if not template_id:
            raise ValueError("template_id is required.")

        url = f"{self.api_url}/api/external/invoices/templates/{template_id}"
        headers = {"X-ApiKey": self.api_key}

        logo = params.get("logo")
        use_multipart = isinstance(logo, (bytes, tuple))

        if use_multipart:
            # Force _method override to PUT
            params["_method"] = "PUT"

            files = {}
            if logo:
                files["logo"] = logo
                params["logo"] = None

            form_data = {"json": json.dumps(params)}
            response = requests.post(url, headers=headers, data=form_data, files=files)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.put(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()
    
    def delete_invoice_template(self, template_id: str) -> dict:
        """
        Delete an invoice template by ID.

        Args:
            template_id (str): The ID of the invoice template to delete.

        Returns:
            dict: API response confirming deletion.
        """
        if not template_id:
            raise ValueError("template_id is required.")

        url = f"{self.api_url}/api/external/invoices/templates/{template_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json() 
    
    def create_invoice_product(self, params: dict) -> dict:
        """
        Create a new product for use in invoices.

        Automatically switches to multipart/form-data if `image` is a file-like object.

        Args:
            params (dict): Product data with possible keys:
                - name (str, required)
                - sku (str, optional)
                - type (str, required): "physical" or "digital"
                - description (str, optional)
                - image (file-like object, optional)
                - prices (list of dicts, optional)

        Returns:
            dict: Created product data from the API.
        """
        url = f"{self.api_url}/api/external/invoices/products"
        headers = {"X-ApiKey": self.api_key}

        image = params.get("image")
        use_multipart = isinstance(image, (bytes, tuple))

        if use_multipart:
            files = {"image": image}
            params["image"] = None  # Remove file reference from params
            form_data = {"json": json.dumps(params)}
            response = requests.post(url, headers=headers, data=form_data, files=files)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.post(url, headers=headers, json=params)

        response.raise_for_status()
        return response.json()
    
    def list_invoice_products(self, params: dict = None) -> dict:
        """
        Retrieve a list of invoice products with optional filters.

        Docs:
            https://docs.fasterpay.com/api#section-list-invoice-products

        Args:
            params (dict, optional): Query parameters for filtering and pagination.
                - include (str): Use 'prices' to include price data in the response.
                - page (int): Page number to retrieve (starting from 1).
                - per_page (int): Number of items per page (max 1000).
                - filter (dict): Object with possible keys:
                    - name (str): Filter by product name.
                    - type (str): Filter by type ('physical' or 'digital').
                    - sku (str): Filter by SKU.
                - prices (dict): Object with possible key:
                    - prices.currency (str): Currency code to filter product prices.

        Returns:
            dict: API response with product list and metadata.
        """
        url = f"{self.api_url}/api/external/invoices/products"
        response = requests.get(url, headers={"X-ApiKey": self.api_key}, params=params or {})
        response.raise_for_status()
        return response.json()
    
    def get_invoice_product(self, product_id: str) -> dict:
        """
        Retrieve details of a specific invoice product by ID.

        Args:
            product_id (str): The ID of the product to retrieve.

        Returns:
            dict: Product details from the API.
        """
        if not product_id:
            raise ValueError("product_id is required.")

        url = f"{self.api_url}/api/external/invoices/products/{product_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def update_invoice_product(self, product_id: str, data: dict, files: dict = None) -> dict:
        """
        Update an invoice product.

        Docs:
            https://docs.fasterpay.com/api#section-update-invoice-product

        Args:
            product_id (str): ID of the product to update (e.g. 'PD-250528-L5CC').
            data (dict): Fields to update:
                - name (str)
                - sku (str)
                - type (str): 'physical' or 'digital'
                - description (str)
                - prices (list of dict): [{price: float, currency: str}]
            files (dict, optional): Use {'image': (filename, fileobj, mimetype)} if an image file is included.

        Returns:
            dict: API response with updated product data.
        """
        url = f"{self.api_url}/api/external/invoices/products/{product_id}"

        headers = {"X-ApiKey": self.api_key}

        if files:
            data["_method"] = "PUT"
            response = requests.post(url, data=data, files=files, headers=headers)
        else:
            response = requests.put(url, json=data, headers=headers)

        response.raise_for_status()
        return response.json()
    
    def delete_invoice_product(self, product_id: str) -> dict:
        """
        Delete an invoice product by ID.

        Args:
            product_id (str): The ID of the product to delete.

        Returns:
            dict: API response confirming deletion.
        """
        if not product_id:
            raise ValueError("product_id is required.")

        url = f"{self.api_url}/api/external/invoices/products/{product_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def delete_invoice_product_price(self, product_id: str, currency: str) -> dict:
        """
        Delete an invoice product price by product ID and currency.

        Args:
            product_id (str): The ID of the product to delete.
            currency (str): The currency code of the price to delete (e.g. 'USD').

        Returns:
            dict: API response confirming deletion.
        """
        if not product_id or not currency:
            raise ValueError("product_id and currency is required.")

        url = f"{self.api_url}/api/external/invoices/products/{product_id}/prices/{currency}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_invoice_tax(self, data: dict) -> dict:
        """
        Create an invoice tax.

        Args:
            data (dict): Tax fields:
                - name (str): Required
                - value (float): Required, min 0.01, max 1000
                - description (str): Optional
                - deleted_at (str): Optional, set to 'true' to permanently delete

        Returns:
            dict: API response with created tax object
        """
        url = f"{self.api_url}/api/external/invoices/taxes"
        headers = {"X-ApiKey": self.api_key}
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def list_invoice_taxes(self, params: dict = None) -> dict:
        """
        Retrieve a list of all invoice taxes, with optional filters and pagination.

        Args:
            params (dict, optional): Query parameters. Can include:
                - page (int)
                - per_page (int, max 1000)
                - filter[name] (str)
                - filter[type] (str)
                - filter[active] (bool)

        Returns:
            dict: API response with list of tax objects
        """
        url = f"{self.api_url}/api/external/invoices/taxes"
        headers = {"X-ApiKey": self.api_key}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_invoice_tax(self, tax_id: str) -> dict:
        """
        Retrieve details of a specific invoice tax by ID.

        Args:
            tax_id (str): The ID of the tax to retrieve.

        Returns:
            dict: API response with tax details.
        """
        if not tax_id:
            raise ValueError("tax_id is required.")

        url = f"{self.api_url}/api/external/invoices/taxes/{tax_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def update_invoice_tax(self, tax_id: str, data: dict) -> dict:
        """
        Update an existing invoice tax by ID.

        Args:
            tax_id (str): ID of the tax to update (e.g. "TX-250527-2E9N")
            data (dict): Tax data to update. Must include:
                - name (str): Required
                - value (float): Required
                - description (str): Optional

        Returns:
            dict: API response with updated tax data
        """
        url = f"{self.api_url}/api/external/invoices/taxes/{tax_id}"
        headers = {"X-ApiKey": self.api_key, "Content-Type": "application/json"}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete_invoice_tax(self, tax_id: str) -> dict:
        """
        Delete an invoice tax by ID.

        Args:
            tax_id (str): The ID of the tax to delete.

        Returns:
            dict: API response confirming deletion.
        """
        if not tax_id:
            raise ValueError("tax_id is required.")

        url = f"{self.api_url}/api/external/invoices/taxes/{tax_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def create_invoice_discount(self, data: dict) -> dict:
        """
        Create a new invoice discount.

        Args:
            data (dict): Discount details, must include:
                - name (str): Required, max 191 characters
                - type (str): Required, "flat" or "percentage"
                - value (float): Required, 0.01–1000
                - currency (str): Required if type is "flat" (ISO 4217 format)
                - description (str): Optional, max 191 characters

        Returns:
            dict: API response with created discount data
        """
        url = f"{self.api_url}/api/external/invoices/discounts"
        headers = {"X-ApiKey": self.api_key, "Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def list_invoice_discounts(self, params: dict = None) -> dict:
        """
        Retrieve a list of all invoice discounts, with optional filters and pagination.

        Args:
            params (dict, optional): Query parameters. Can include:
                - page (int)
                - per_page (int, max 1000)
                - filter[name] (str)
                - filter[type] (str)
                - filter[active] (bool)
                - filter[currency] (str): ISO 4217 format for flat discounts

        Returns:
            dict: API response with list of discount objects
        """
        url = f"{self.api_url}/api/external/invoices/discounts"
        headers = {"X-ApiKey": self.api_key}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_invoice_discount(self, discount_id: str) -> dict:
        """
        Retrieve details of a specific invoice discount by ID.

        Args:
            discount_id (str): The ID of the discount to retrieve.

        Returns:
            dict: API response with discount details.
        """
        if not discount_id:
            raise ValueError("discount_id is required.")

        url = f"{self.api_url}/api/external/invoices/discounts/{discount_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def update_invoice_discount(self, discount_id: str, data: dict) -> dict:
        """
        Update an existing invoice tax by ID.

        Args:
            discount_id (str): ID of the discount to update (e.g. "TX-250527-2E9N")
            data (dict): Tax data to update.
                - name (str): Optional
                - type (enum): Optional, "flat" or "percentage"
                - value (float): Optional
                - currency (str): Optional, required if type is "flat" (ISO 4217 format)
                - description (str): Optional

        Returns:
            dict: API response with updated tax data
        """
        url = f"{self.api_url}/api/external/invoices/discounts/{discount_id}"
        headers = {"X-ApiKey": self.api_key, "Content-Type": "application/json"}
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete_invoice_discount(self, discount_id: str) -> dict:
        """
        Delete an invoice discount by ID.

        Args:
            discount_id (str): The ID of the discount to delete.

        Returns:
            dict: API response confirming deletion.
        """
        if not discount_id:
            raise ValueError("discount_id is required.")

        url = f"{self.api_url}/api/external/invoices/discounts/{discount_id}"
        headers = {"X-ApiKey": self.api_key}

        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()