"""Shop blueprint for displaying products and shop functionality."""

from flask import Blueprint, render_template

# Create shop blueprint
shop_bp = Blueprint('shop_bp', __name__)


@shop_bp.route('/shop')
def shop():
    """Shop page displaying products grid."""
    
    # Placeholder product data
    products = [
        {
            'id': 1,
            'name': 'Premium Dog Food',
            'price': 49.99,
            'image': '🍖',
            'description': 'High-quality nutrition for your furry friend'
        },
        {
            'id': 2,
            'name': 'Cat Grooming Kit',
            'price': 29.99,
            'image': '🧴',
            'description': 'Complete grooming essentials for cats'
        },
        {
            'id': 3,
            'name': 'Pet Toy Set',
            'price': 19.99,
            'image': '🎾',
            'description': 'Fun and interactive toys for pets'
        },
        {
            'id': 4,
            'name': 'Pet Carrier',
            'price': 79.99,
            'image': '🎒',
            'description': 'Safe and comfortable travel carrier'
        },
        {
            'id': 5,
            'name': 'Pet Bed',
            'price': 39.99,
            'image': '🛏️',
            'description': 'Cozy and comfortable pet bed'
        },
        {
            'id': 6,
            'name': 'Dog Leash',
            'price': 15.99,
            'image': '🦮',
            'description': 'Durable and comfortable dog leash'
        }
    ]
    
    return render_template('shop.html', products=products)