# Thanamani Textiles Management System

A modern, responsive textile management system built with Flask and MongoDB, featuring a comprehensive admin dashboard and dynamic dress management.

## 🚀 Features

### ✨ User Features
- **Responsive Design**: Modern, mobile-friendly interface
- **Advanced Filtering**: Search by name, type, color, and price range
- **Dynamic Dress Display**: Real-time dress listings with smooth animations
- **User Authentication**: Secure login/signup system
- **Order Management**: Complete order placement and tracking
- **Review System**: User reviews and ratings for dresses
- **Password Recovery**: Email-based password reset functionality

### 🔧 Admin Features
- **Comprehensive Dashboard**: Real-time statistics and analytics
- **Advanced Dress Management**: Full CRUD operations with rich metadata
- **Order Management**: Complete order lifecycle management
- **User Management**: User administration and role management
- **Review Management**: Moderate and manage user reviews
- **Revenue Analytics**: Sales tracking and financial insights

### 🎨 Design Improvements
- **Modern UI/UX**: Beautiful gradient backgrounds and glassmorphism effects
- **Responsive Layout**: Works perfectly on all device sizes
- **Smooth Animations**: Engaging user interactions and transitions
- **Indian Rupee Support**: All prices displayed in ₹ (Indian Rupees)
- **Accessibility**: Improved contrast and keyboard navigation

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Frontend**: HTML5, CSS3, JavaScript
- **Styling**: Custom CSS with modern design patterns
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Poppins, Dancing Script)

## 📦 Installation

### Prerequisites
- Python 3.7+
- MongoDB
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd textiles
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Ensure MongoDB is running on your system
   - The application will automatically create the required collections

5. **Set up environment variables** (optional)
   ```bash
   # For email functionality
   export EMAIL_USER="your-email@gmail.com"
   export EMAIL_PASS="your-app-password"
   
   # For Flask secret keys
   export FLASK_SECRET_KEY="your-secret-key"
   ```

6. **Run the application**
   ```bash
   # Run both main app and admin panel
   python run_app.py
   
   # Or run individually
   python app.py          # Main app on port 5000
   python admin.py        # Admin panel on port 5001
   ```

## 🌐 Access Points

- **Main Application**: http://localhost:5000
- **Admin Dashboard**: http://localhost:5001
- **API Endpoints**: Available for dynamic content loading

## 📊 Admin Dashboard Features

### Statistics Overview
- Total users, dresses, orders, and reviews
- Revenue analytics (last 30 days)
- Order status breakdown
- Popular dress types

### Recent Activity
- Latest orders with status indicators
- Recently added dresses
- Real-time updates

### Management Tools
- **Dress Management**: Add, edit, delete dresses with rich metadata
- **Order Management**: Update order status, track deliveries
- **User Management**: Admin role management
- **Review Management**: Moderate user feedback

## 👗 Dress Management

### Enhanced Dress Fields
- **Basic Info**: Name, type, color, price
- **Details**: Gender, size, material, brand
- **Inventory**: Stock quantity tracking
- **Media**: High-quality image uploads
- **Description**: Rich text descriptions

### Advanced Filtering
- Search by name or description
- Filter by dress type and color
- Price range filtering
- Real-time search with debouncing

## 🔒 Security Features

- **Password Hashing**: Secure password storage
- **Session Management**: Secure user sessions
- **Input Validation**: Comprehensive form validation
- **File Upload Security**: Secure image upload handling
- **Admin Authentication**: Protected admin routes

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface for small screens

## 🎯 Key Improvements Made

### 1. **Responsive Design**
- Mobile-first approach
- Flexible grid layouts
- Touch-friendly interactions
- Optimized for all screen sizes

### 2. **Error Correction**
- Fixed form validation issues
- Improved error handling
- Better user feedback
- Robust data validation

### 3. **Currency Conversion**
- Changed from USD to Indian Rupees (₹)
- Updated all price displays
- Consistent currency formatting

### 4. **Admin Dashboard Enhancement**
- Comprehensive statistics
- Real-time data updates
- Advanced filtering capabilities
- Better user management

### 5. **Dynamic Dress Display**
- Real-time dress loading
- Advanced search functionality
- Smooth animations
- Better image handling

## 🚀 API Endpoints

### Public APIs
- `GET /api/dresses` - Get all dresses
- `GET /api/dress/<id>` - Get specific dress
- `GET /api/search?q=<query>` - Search dresses

### Admin APIs
- `GET /api/dashboard/stats` - Dashboard statistics
- `GET /api/dresses/search` - Admin dress search

## 📁 Project Structure

```
textiles/
├── app.py                 # Main Flask application
├── admin.py              # Admin panel application
├── run_app.py            # Application launcher
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── static/              # Static assets
│   ├── styles.css       # Main stylesheet
│   ├── dress/           # Dress images
│   └── uploads/         # User uploaded images
├── template/            # Main app templates
│   ├── index.html       # Dress listing page
│   ├── dress_detail.html # Dress detail page
│   └── ...              # Other templates
└── admin_template/      # Admin panel templates
    ├── admin_dashboard.html # Admin dashboard
    ├── admin_dresses.html   # Dress management
    ├── add_dress.html       # Add dress form
    └── ...                  # Other admin templates
```

## 🔧 Configuration

### Environment Variables
```bash
# Email Configuration (for password reset)
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password

# Flask Configuration
FLASK_SECRET_KEY=your-secret-key
MONGODB_URI=mongodb://localhost:27017/

# Optional: Debug mode
FLASK_DEBUG=True
```

### Database Collections
The application automatically creates these MongoDB collections:
- `login` - User accounts
- `dress` - Dress inventory
- `confirmed_order` - Order management
- `reviews` - User reviews

## 🐛 Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB is running
   - Check connection string in app.py

2. **Image Upload Issues**
   - Verify uploads directory exists
   - Check file permissions
   - Ensure valid image formats

3. **Email Not Working**
   - Configure email environment variables
   - Use app-specific passwords for Gmail
   - Check SMTP settings

### Debug Mode
Enable debug mode for development:
```bash
export FLASK_DEBUG=True
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework for the web framework
- MongoDB for the database
- Font Awesome for icons
- Google Fonts for typography
- Modern CSS techniques for responsive design

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

---

**Thanamani Textiles Management System** - Modern, responsive, and feature-rich textile management solution. 