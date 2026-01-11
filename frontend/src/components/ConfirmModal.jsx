const ConfirmModal = ({ open, onClose, onConfirm, title }) => {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-[400px]">
        <h2 className="text-lg font-semibold text-gray-800">
          Delete Job Description?
        </h2>

        <p className="mt-3 text-gray-600">
          Are you sure you want to delete{" "}
          <span className="font-semibold">{title}</span>?
        </p>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded-lg"
          >
            Cancel
          </button>

          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-600 text-white rounded-lg"
          >
            Yes, Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default ConfirmModal;