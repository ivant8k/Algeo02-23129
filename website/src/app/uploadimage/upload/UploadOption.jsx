import * as React from "react";

export function UploadOption({ icon, label, onClick }) {
  return (
    <div
      className="upload-option"
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyPress={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          onClick();
        }
      }}
    >
      <img
        loading="lazy"
        src={icon}
        alt={`${label} upload option icon`}
        className="option-icon"
      />
      <div className="option-label">{label}</div>
    </div>
  );
}
