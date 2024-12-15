import * as React from "react";
import { styles } from "./styles";
import { UploadOption } from "./UploadOption";

const uploadOptions = [
  {
    icon: "https://cdn.builder.io/api/v1/image/assets/3f4b31c8990a4ddea61495c8cf9886e2/d27b1bd8bab2f564fb43ddcf10fd1d7c3c263a3188476d3fe8f63d15e62e0221?apiKey=3f4b31c8990a4ddea61495c8cf9886e2&",
    label: "AUDIO",
  },
  {
    icon: "https://cdn.builder.io/api/v1/image/assets/3f4b31c8990a4ddea61495c8cf9886e2/5f5c46f34e3208ae1e0ab601978af27f530574473b41763896c12045345f8100?apiKey=3f4b31c8990a4ddea61495c8cf9886e2&",
    label: "IMAGE",
  },
];

export function UploadPage() {
  const handleOptionClick = (optionType) => {
    console.log(`Selected ${optionType} upload`);
  };

  return (
    <main className="upload-container">
      <header className="header">
        <img
          loading="lazy"
          src="https://cdn.builder.io/api/v1/image/assets/3f4b31c8990a4ddea61495c8cf9886e2/63162e32fa7a33e30c6dc2aaee84d85767b56647eb7a9da95861ce9db5414c15?apiKey=3f4b31c8990a4ddea61495c8cf9886e2&"
          alt="Website logo"
          className="logo"
        />
        <h1 className="site-title">&lt;JUDUL WEBSITE&gt;</h1>
      </header>

      <section
        className="content-wrapper"
        role="region"
        aria-label="File upload section"
      >
        <div className="upload-section">
          <h2 className="section-title">
            Choose the type of file you want to upload
          </h2>

          <div className="options-container">
            <div className="options-grid">
              {uploadOptions.map((option, index) => (
                <div key={index} style={{ width: "50%" }}>
                  <UploadOption
                    icon={option.icon}
                    label={option.label}
                    onClick={() => handleOptionClick(option.label)}
                  />
                </div>
              ))}
            </div>
          </div>

          <button
            className="next-button"
            onClick={() => console.log("Next clicked")}
            aria-label="Proceed to next step"
          >
            NEXT
          </button>
        </div>
      </section>
      <style jsx>{styles}</style>
    </main>
  );
}
