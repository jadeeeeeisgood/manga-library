class StatusMapping:
    STATUS_MAP = {
        # Vietnamese to English
        'Đang tiến hành': 'Publishing',
        'Hoàn thành': 'Completed',
        'Tạm ngừng': 'On Hiatus',
        
        # English to Vietnamese
        'Publishing': 'Đang tiến hành',
        'Completed': 'Hoàn thành',
        'Finished': 'Hoàn thành',
        'Complete': 'Hoàn thành',
        'On Hiatus': 'Tạm ngừng',
        'Hiatus': 'Tạm ngừng',
        'Ongoing': 'Đang tiến hành',
        'Currently Publishing': 'Đang tiến hành',
        'Discontinued': 'Tạm ngừng',
        'Not yet published': 'Đang tiến hành'
    }

    @staticmethod
    def to_vietnamese(status):
        """Convert status to Vietnamese"""
        if not status:
            return 'Không xác định'
        status = status.strip()
        return StatusMapping.STATUS_MAP.get(status, 'Không xác định')

    @staticmethod
    def to_english(status):
        """Convert status to English"""
        if not status:
            return 'Unknown'
        status = status.strip()
        if status in StatusMapping.STATUS_MAP:
            for eng, viet in StatusMapping.STATUS_MAP.items():
                if viet == status:
                    return eng
        return 'Unknown'

    @staticmethod
    def get_vietnamese_statuses():
        """Get list of Vietnamese statuses"""
        return ['Đang tiến hành', 'Hoàn thành', 'Tạm ngừng']

    @staticmethod
    def normalize_status(status):
        """Normalize any status to Vietnamese format"""
        if not status:
            return 'Không xác định'
        status = status.strip()
        
        # If already in Vietnamese, return as is if valid
        if status in ['Đang tiến hành', 'Hoàn thành', 'Tạm ngừng']:
            return status
            
        # Try to convert from English
        return StatusMapping.to_vietnamese(status)
