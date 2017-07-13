from . import addTimeToModel, db, db_insert, db_update, db_delete, db_commit, db_persist
from ..utils.file_upload import product_images_upload, delete_file


@addTimeToModel
class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Numeric(10, 2))
    number = db.Column(db.Integer)
    detail = db.Column(db.Text)
    tips = db.Column(db.Text)  # add for search speed
    is_pub = db.Column(db.Boolean, default=True)
    is_hot = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # relations
    category = db.relationship("Category", back_populates="products")
    product_images = db.relationship(
        'ProductImage', back_populates='product', lazy='dynamic')
    order_details = db.relationship(
        'OrderDetail', back_populates='product', lazy='dynamic')

    def save_product_images(self, files):
        from . import ProductImage

        for image in files:
            filename = product_images_upload.save(image)
            product_image = ProductImage().save(filename, self.id)
            db_persist(product_image)

        db_commit()
