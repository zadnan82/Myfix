# sevdo_frontend/prefabs/add_to_cart.py
def render_prefab(args, props):
    # Defaults
    title = props.get("title", "Your Cart")
    empty_text = props.get("emptyText", "Your cart is empty.")
    checkout_text = props.get("checkoutText", "Checkout")
    clear_text = props.get("clearText", "Clear")
    currency = props.get("currency", "$")
    cart_key = props.get("cartKey", "sevdoCart")

    # Optional backend props
    checkout_path = props.get("checkoutPath")
    checkout_method = (props.get("checkoutMethod") or "POST").upper()
    checkout_action = props.get("checkoutAction")

    # Nested overrides
    if args:
        import sys
        import os
        parent_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__)))
        if parent_dir not in sys.path:
            sys.path.append(parent_dir)
        from frontend_compiler import parse_dsl
        try:
            nodes = parse_dsl(args)
            if nodes:
                for node in nodes:
                    if node.token == "h" and node.args:
                        title = node.args
                    elif node.token == "b" and node.args:
                        checkout_text = node.args
        except Exception:
            title = args

    # Generate React component with proper hooks instead of DOM manipulation
    # Use safe string formatting to avoid f-string conflicts

    # Create the JavaScript template using string concatenation
    js_template = '''
import { useState, useEffect } from 'react';

function CartContent() {
    const [cart, setCart] = useState([]);
    const [total, setTotal] = useState(0);

    // Load cart from localStorage on mount
    useEffect(() => {
        try {
            const storedCart = JSON.parse(localStorage.getItem(''' + repr(cart_key) + ''' || '[]');
            setCart(storedCart);
            updateTotal(storedCart);
        } catch (e) {
            console.error('Error loading cart:', e);
            setCart([]);
            setTotal(0);
        }
    }, []);

    // Update total when cart changes
    const updateTotal = (cartItems) => {
        const newTotal = cartItems.reduce((sum, item) => sum + Number(item.price || 0), 0);
        setTotal(newTotal);
    };

    // Save cart to localStorage
    const saveCart = (newCart) => {
        localStorage.setItem(''' + repr(cart_key) + ''', JSON.stringify(newCart));
        setCart(newCart);
        updateTotal(newCart);
    };

    // Clear cart
    const handleClearCart = () => {
        saveCart([]);
        if (window.sevdoAct) {
            window.sevdoAct('api:POST /api/echo|' + JSON.stringify({event: 'cart_clear', ts: Date.now()}));
        }
    };

    // Checkout
    const handleCheckout = () => {
        if (''' + repr(checkout_action) + ''') {
            if (window.sevdoAct) {
                window.sevdoAct(''' + repr(checkout_action) + ''');
            }
        } else {
            const endpoint = ''' + (repr(checkout_path) if checkout_path else '"/api/echo"') + ''';
            if (window.sevdoAct) {
                window.sevdoAct('api:' + ''' + repr(checkout_method) + ''' + ' ' + endpoint + '|' + JSON.stringify({event: 'checkout', cart: cart, ts: Date.now()}));
            }
        }
    };

    // Remove item from cart
    const removeItem = (index) => {
        const newCart = cart.filter((_, i) => i !== index);
        saveCart(newCart);
    };

    return (
        <div className="max-w-3xl mx-auto px-4">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">
                    ''' + repr(title) + ''' <span className="ml-2 text-sm text-gray-500">(Items: {cart.length})</span>
                </h2>
                <div className="flex gap-2">
                    <button
                        onClick={handleClearCart}
                        className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium px-3 py-1.5 rounded text-sm transition-colors"
                    >
                        ''' + repr(clear_text) + '''
                    </button>
                    <button
                        onClick={handleCheckout}
                        className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-3 py-1.5 rounded text-sm transition-colors"
                    >
                        ''' + repr(checkout_text) + '''
                    </button>
                </div>
            </div>
            <div className="mb-3 text-right text-gray-700">
                Total: <strong>''' + repr(currency) + '''{total.toFixed(2)}</strong>
            </div>
            <div className="divide-y divide-gray-200">
                {cart.length === 0 ? (
                    <div className="text-gray-400 italic py-4">''' + repr(empty_text) + '''</div>
                ) : (
                    cart.map((item, index) => (
                        <div key={index} className="flex items-center justify-between py-2">
                            <div className="flex items-center gap-3">
                                {item.image && (
                                    <img
                                        src={item.image}
                                        alt={item.name || ''}
                                        className="w-10 h-10 rounded object-cover"
                                    />
                                )}
                                <div>
                                    <div className="font-medium">{item.name || ''}</div>
                                    <div className="text-sm text-gray-500">''' + repr(currency) + '''{Number(item.price || 0).toFixed(2)}</div>
                                </div>
                            </div>
                            <div className="flex items-center gap-3">
                                <div className="text-sm text-gray-700">''' + repr(currency) + '''{Number(item.price || 0).toFixed(2)}</div>
                                <button
                                    onClick={() => removeItem(index)}
                                    className="text-red-500 hover:text-red-700 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default function AddToCart() {
    return (
        <section className="py-6 bg-white border rounded-lg">
            <CartContent />
        </section>
    );
}'''

    return js_template


# Register with token "ac"
COMPONENT_TOKEN = "ac"