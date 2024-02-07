from .base import ModuleTestBase


class TestNewsletters(ModuleTestBase):
    found_tgt = "http://127.0.0.1:8888/found"
    missing_tgt = "http://127.0.0.1:8888/missing"
    targets = [found_tgt, missing_tgt]
    modules_overrides = ["speculate", "httpx", "newsletters"]

    html_with_newsletter = """
    <input aria-required="true" 
    class="form-input form-input-text required" 
    data-at="form-email" 
    data-describedby="form-validation-error-box-element-5" 
    data-label-inside="Enter your email" 
    id="field-5f329905b4bfe1027b44513f94b50363-0" 
    name="Enter your email" 
    placeholder="Enter your email" 
    required="" 
    title="Enter your email" 
    type="email" value=""/>
    """

    html_without_newsletter = """
    <div>
    <h1>Example Domain</h1>
    <p>This domain is for use in illustrative examples in documents. You may use this
    domain in literature without prior coordination or asking for permission.</p>
    <p><a href="https://www.iana.org/domains/example">More information...</a></p>
    </div>
    """

    async def setup_after_prep(self, module_test):
        request_args = dict(uri="/found", headers={"test": "header"})
        respond_args = dict(response_data=self.html_with_newsletter)
        module_test.set_expect_requests(request_args, respond_args)
        request_args = dict(uri="/missing", headers={"test": "header"})
        respond_args = dict(response_data=self.html_without_newsletter)
        module_test.set_expect_requests(request_args, respond_args)

    def check(self, module_test, events):
        count = 0
        for event in events:
            if event.type == "NEWSLETTER":
                # Verify Positive Result
                if event.data == self.found_tgt:
                    count += 1
                # Verify Negative Result (should skip this statement if correct)
                elif event.data == self.missing_tgt:
                    count += -1
        assert count == 1, f"NEWSLETTER Error - Expect count of 1 but got {count}"